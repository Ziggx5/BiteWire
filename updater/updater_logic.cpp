#include "updater.h"
#include <iostream>
#include <qstring.h>
#include <QDir>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QProcess>
#include <QCryptographicHash>
#include <QStorageInfo>
#include <QStandardPaths>
#include <QDateTime>
#include <QTextStream>
#include <QTimer>

UpdaterLogic::UpdaterLogic(QObject *parent) : QObject(parent) {

}

void UpdaterLogic::downloadUpdate(const QString &downloadUrl, const QString &currentSystem, const QString &bitewirePath, const QString &sha256, qint64 updateSize, const QString &appDirectory) {
    QStorageInfo storage(QDir::tempPath());
    qint64 bytesAvailable = storage.bytesAvailable();

    if (bytesAvailable <= 0) {
        emit setStatus("Unable to determine free disk space");
        emit closeUpdater();
        return;
    }

    if (bytesAvailable < static_cast<qint64>(updateSize * 1.1)) {
        emit setStatus("Not enough free disk space");
        emit closeUpdater();
        return;
    }

    QUrl url(downloadUrl);

    if (url.scheme() != "https") {
        emit setStatus("Insecure download URL");
        emit closeUpdater();
        return;
    }

    QNetworkRequest request(url);
    request.setAttribute(QNetworkRequest::RedirectPolicyAttribute, QNetworkRequest::NoLessSafeRedirectPolicy);

    QString fileName = QFileInfo(url.path()).fileName();
    QString savePath = QDir::tempPath() + "/" + fileName;

    QNetworkAccessManager *manager = new QNetworkAccessManager(this);

    QNetworkReply *reply = manager->get(request);

    QTimer *timeoutTimer = new QTimer(reply);
    timeoutTimer->setSingleShot(true);
    timeoutTimer->start(20000);

    QObject::connect(timeoutTimer, &QTimer::timeout, reply, &QNetworkReply::abort);

    QObject::connect(reply, &QNetworkReply::downloadProgress, timeoutTimer, [timeoutTimer] () {
        timeoutTimer->start(20000);
    });

    QObject::connect(reply, &QNetworkReply::downloadProgress, this, &UpdaterLogic::downloadProgress);

    QObject::connect(reply,  &QNetworkReply::finished, [reply, manager, savePath, this, currentSystem, bitewirePath, sha256, timeoutTimer, appDirectory]() {
        timeoutTimer->stop();

        int httpStatus = reply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();

        if (reply->error() != QNetworkReply::NoError) {
            QFile::remove(savePath);
            QString statusText;

            if (reply->error() == QNetworkReply::OperationCanceledError) {
                statusText = "Download timed out";
            }

            else if (httpStatus == 404) {
                statusText = "Update file not found (404)";
            }
            else if (httpStatus == 403) {
                statusText = "Access denied (403)";
            }
            else if (httpStatus >= 500) {
                statusText = QString("GitHub server error (%1)").arg(httpStatus);
            }
            else {
                statusText = "Download failed";
            }

            emit setStatus(statusText);
            logMessage("ERROR", "Can't download file", reply->errorString(), appDirectory);
            emit closeUpdater();

            reply->deleteLater();
            manager->deleteLater();

            return;
        }

        QFile file(savePath);

        if (!file.open(QIODevice::WriteOnly)) {
            file.remove();

            emit setStatus("File write error");
            logMessage("ERROR", "Can't open file for writing", file.errorString(), appDirectory);
            emit closeUpdater();

            reply->deleteLater();
            manager->deleteLater();
            return;
        }

        QByteArray data = reply->readAll();

        if (file.write(data) != data.size()) {
            file.close();
            file.remove();

            emit setStatus("File write error");
            logMessage("ERROR", "Incomplete file write", file.errorString(), appDirectory);
            emit closeUpdater();

            reply->deleteLater();
            manager->deleteLater();
            return;
        }

        file.close();

        reply->deleteLater();
        manager->deleteLater();

        if (calculateSha256(sha256, file, appDirectory)) {
            emit downloadFinished();
            QTimer::singleShot(2000, this, [this, currentSystem, savePath, bitewirePath, appDirectory]() {
            updateApp(currentSystem, savePath, bitewirePath, appDirectory);
        });
        }
    }
    );
}

void UpdaterLogic::downloadProgress(qint64 bytesReceived, qint64 bytesTotal) {
    if (bytesTotal <= 0)
        return;

    int percent = static_cast<int>(bytesReceived * 100 / bytesTotal);

    double receivedMB = bytesReceived / (1024.0 * 1024.0);
    double totalMB = bytesTotal / (1024.0 * 1024.0);

    emit progressChanged(percent, receivedMB, totalMB);
}

void UpdaterLogic::updateApp(const QString &currentSystem, const QString &savePath, const QString &bitewirePath, const QString &appDirectory) {
    if (currentSystem == "windows") {
        QString fileDirectory = QFileInfo(bitewirePath).absolutePath();
        QString unZipDirectory = QDir::tempPath() + "/BiteWireUpdate";

        extractZip(savePath, unZipDirectory, fileDirectory, appDirectory);
    }
    else if (currentSystem == "linux") {
        if (savePath.endsWith(".rpm")) {
            QStringList arguments;
            arguments << "dnf5" << "install" << "-y" << savePath;

            updateLinuxApp(arguments, savePath, appDirectory);
        }
        else if (savePath.endsWith(".deb")) {
            QStringList arguments;
            arguments << "apt" << "install" << "-y" << savePath;
            updateLinuxApp(arguments, savePath, appDirectory);
        }
        else {
            QFile::remove(savePath);

            emit setStatus("Update failed");
            logMessage("ERROR", "Unrecognised file format", savePath, appDirectory);
            emit closeUpdater();
        }
    }
    else {
        QFile::remove(savePath);

        emit setStatus("Update failed");
        logMessage("ERROR", "Unsupported operating system", currentSystem, appDirectory);
        emit closeUpdater();
    }
}

void UpdaterLogic::extractZip(const QString &savePath, const QString &unZipDirectory, const QString &appDirectory, const QString &localFilePath) {
    QDir dir(unZipDirectory);

    if (dir.exists()) {
        dir.removeRecursively();
    }

    QDir().mkpath(unZipDirectory);

    QProcess *process = new QProcess(this);

    QObject::connect(process, &QProcess::finished, this, [this, process, unZipDirectory, appDirectory, savePath, localFilePath](int exitCode, QProcess::ExitStatus exitStatus) {
        if (exitCode == 0 && exitStatus == QProcess::NormalExit) {
            updateWindowsApp(unZipDirectory, appDirectory, savePath, localFilePath);
        }
        else {
            emit setStatus("Update failed");
            logMessage("ERROR", "PowerShell Expand-Archive failed, exit code" + QString::number(exitCode), QString::fromUtf8(process->readAllStandardError()), localFilePath);
            emit closeUpdater();
        }

        process->deleteLater();
    });

    QStringList arguments;

    arguments << "-NoProfile" << "-NonInteractive" << "-Command" << QString("Expand-Archive -LiteralPath '%1' -DestinationPath '%2' -Force").arg(savePath, unZipDirectory);

    process->start("powershell.exe", arguments);
}

void UpdaterLogic::updateWindowsApp(const QString &unZipDirectory, const QString &appDirectory, const QString &savePath, const QString &localFilePath) {
    QProcess *process = new QProcess(this);

    QObject::connect(process, &QProcess::finished, this, [this, process, savePath, unZipDirectory, localFilePath](int exitCode, QProcess::ExitStatus exitStatus) {
        QString statusText;

        if (exitCode == 0 && exitStatus == QProcess::NormalExit) {
            statusText = "Update successful";
        }
        else {
            statusText = "Update failed";
            logMessage("ERROR", "PowerShell Copy-Item failed, exit code" + QString::number(exitCode), QString::fromUtf8(process->readAllStandardError()), localFilePath);
        }

        QFile::remove(savePath);
        QDir(unZipDirectory).removeRecursively();

        emit setStatus(statusText);
        emit closeUpdater();

        process->deleteLater();
    });

    QStringList arguments;

    arguments << "-NoProfile" << "-NonInteractive" << "-Command" << QString("Copy-Item -Path '%1\\*' -Destination '%2' -Recurse -Force").arg(unZipDirectory, appDirectory);

    process->start("powershell.exe", arguments);
}

void UpdaterLogic::updateLinuxApp(const QStringList &arguments, const QString &savePath, const QString &localFilePath) {
    QProcess *process = new QProcess(this);

    QObject::connect(process, &QProcess::finished, process, &QProcess::deleteLater);
    QObject::connect(process, &QProcess::finished, [this, savePath, process, localFilePath](int exitCode, QProcess::ExitStatus exitStatus) {
        QString statusText;

        if (exitCode ==0 && exitStatus == QProcess::NormalExit) {
            statusText = "Update successful";
        }
        else {
            statusText = "Update failed";
            logMessage("ERROR", "pkexec failed, exit code" + QString::number(exitCode), QString::fromUtf8(process->readAllStandardError()), localFilePath);
        }

        QFile::remove(savePath);

        emit setStatus(statusText);
        emit closeUpdater();
    });

    process->start("pkexec", arguments);
}

bool UpdaterLogic::calculateSha256(const QString &sha256, QFile &file, const QString &appDirectory) {
    emit setStatus("Calculating sha256");

    if (!file.open(QIODevice::ReadOnly)) {
        emit setStatus("Can't read file");
        logMessage("ERROR", "Can't open file for reading", file.errorString(), appDirectory);
        emit closeUpdater();
        return false;
    }

    QCryptographicHash hash(QCryptographicHash::Sha256);

    while (!file.atEnd()) {
        hash.addData(file.read(1024 * 1024));
    }

    file.close();

    if (sha256.toLower() == hash.result().toHex().toLower()) {
        emit setStatus("SHA-256 valid");
        return true;
    }
    else {
        file.remove();

        emit setStatus("SHA-256 mismatch");
        logMessage("ERROR", "Hash mismatch", file.errorString(), appDirectory);
        emit closeUpdater();

        return false;
    }
}

void UpdaterLogic::logMessage(const QString &level, const QString &stage, const QString &message, const QString &appDirectory) {
    QFile file(appDirectory + "/Updater_log.txt");
    if (!file.open(QIODevice::Append | QIODevice::Text)) {
        return;
    }

    QTextStream out(&file);
    out << QDateTime::currentDateTime().toString("yyyy-MM-dd HH:mm:ss") << " [ " << level << " ] " << stage << ":" << "\n";

    if (!message.trimmed().isEmpty()) {
        const QStringList lines = message.trimmed().split("\n");

        for (const QString &line : lines) {
            out << "    " << line << "\n";
        }
    }
}