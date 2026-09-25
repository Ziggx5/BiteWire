#include "updater.h"
#include <iostream>
#include <qstring.h>
#include <QDir>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QProcess>
#include <QCryptographicHash>

UpdaterLogic::UpdaterLogic(QObject *parent) : QObject(parent) {

}

void UpdaterLogic::downloadUpdate(const QString &downloadUrl, const QString &currentSystem, const QString &bitewirePath, const QString &sha256) {
    QUrl url(downloadUrl);

    QString fileName = QFileInfo(url.path()).fileName();
    QString savePath = QDir::tempPath() + "/" + fileName;

    QNetworkAccessManager *manager = new QNetworkAccessManager();

    QNetworkReply *reply = manager->get(QNetworkRequest(url));

    QObject::connect(reply, &QNetworkReply::downloadProgress, this, &UpdaterLogic::downloadProgress);

    QObject::connect(reply,  &QNetworkReply::finished, [reply, manager, savePath, this, currentSystem, bitewirePath, sha256]() {

        int httpStatus = reply->attribute(QNetworkRequest::HttpStatusCodeAttribute).toInt();

        if (reply->error() != QNetworkReply::NoError) {
            QFile::remove(savePath);

            if (httpStatus == 404) {
                emit setStatus("Update file not found (404)");
            }
            else if (httpStatus == 403) {
                emit setStatus("Access denied (403)");
            }
            else if (httpStatus >= 500) {
                emit setStatus(QString("GitHub server error (%1)").arg(httpStatus));
            }
            else {
                emit setStatus("Download failed");
            }

            emit closeUpdater();

            reply->deleteLater();
            manager->deleteLater();
            return;
        }

        QFile file(savePath);

        if (!file.open(QIODevice::WriteOnly)) {
            emit setStatus("File write error");
            file.remove();
            reply->deleteLater();
            manager->deleteLater();

            emit closeUpdater();
            return;
        }

        QByteArray data = reply->readAll();

        if (file.write(data) != data.size()) {
            file.close();
            file.remove();

            emit setStatus("File write error");
            emit closeUpdater();

            reply->deleteLater();
            manager->deleteLater();
            return;
        }

        file.close();

        reply->deleteLater();
        manager->deleteLater();

        if (calculateSha256(sha256, file)) {
            emit downloadFinished();
            QTimer::singleShot(2000, this, [this, currentSystem, savePath, bitewirePath]() {
            updateApp(currentSystem, savePath, bitewirePath);
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

void UpdaterLogic::updateApp(const QString &currentSystem, const QString &savePath, const QString &bitewirePath) {
    if (currentSystem == "windows") {
        QString appDirectory = QFileInfo(bitewirePath).absolutePath();
        QString unZipDirectory = QDir::tempPath() + "/BiteWireUpdate";

        extractZip(savePath, unZipDirectory, appDirectory);
    }
    else if (currentSystem == "linux") {
        if (savePath.endsWith(".rpm")) {
            QStringList arguments;
            arguments << "dnf5" << "install" << "-y" << savePath;

            updateLinuxApp(arguments, savePath);
        }
        else if (savePath.endsWith(".deb")) {
            QStringList arguments;
            arguments << "apt" << "install" << "-y" << savePath;
            updateLinuxApp(arguments, savePath);
        }
        else {
            emit setStatus("Update failed");
            QFile::remove(savePath);
            emit closeUpdater();
        }
    }
    else {
        emit setStatus("Update failed");
        QFile::remove(savePath);
        emit closeUpdater();
    }
}

void UpdaterLogic::extractZip(const QString &savePath, const QString &unZipDirectory, const QString &appDirectory) {
    QDir dir(unZipDirectory);

    if (dir.exists()) {
        dir.removeRecursively();
    }

    QDir().mkpath(unZipDirectory);

    QProcess *process = new QProcess(this);

    QObject::connect(process, &QProcess::finished, this, [this, process, unZipDirectory, appDirectory, savePath](int exitCode, QProcess::ExitStatus exitStatus) {
        if (exitCode == 0 && exitStatus == QProcess::NormalExit) {
            updateWindowsApp(unZipDirectory, appDirectory, savePath);
        }
        else {
            emit setStatus("Update failed");
            emit closeUpdater();
        }

        process->deleteLater();
    });

    QStringList arguments;

    arguments << "-NoProfile" << "-NonInteractive" << "-Command" << QString("Expand-Archive -LiteralPath '%1' -DestinationPath '%2' -Force").arg(savePath, unZipDirectory);

    process->start("powershell.exe", arguments);
}

void UpdaterLogic::updateWindowsApp(const QString &unZipDirectory, const QString &appDirectory, const QString &savePath) {
    QProcess *process = new QProcess(this);

    QObject::connect(process, &QProcess::finished, this, [this, process, savePath, unZipDirectory](int exitCode, QProcess::ExitStatus exitStatus) {
        if (exitCode == 0 && exitStatus == QProcess::NormalExit) {
            emit setStatus("Update successful");
        }
        else {
            emit setStatus("Update failed");
        }

        QFile::remove(savePath);
        QDir(unZipDirectory).removeRecursively();

        emit closeUpdater();

        process->deleteLater();
    });

    QStringList arguments;

    arguments << "-NoProfile" << "-NonInteractive" << "-Command" << QString("Copy-Item -Path '%1\\*' -Destination '%2' -Recurse -Force").arg(unZipDirectory, appDirectory);

    process->start("powershell.exe", arguments);
}

void UpdaterLogic::updateLinuxApp(const QStringList &arguments, const QString &savePath) {
    QProcess *process = new QProcess(this);

    QObject::connect(process, &QProcess::finished, process, &QProcess::deleteLater);
    QObject::connect(process, &QProcess::finished, [this, savePath](int exitCode, QProcess::ExitStatus exitStatus) {
        if (exitCode ==0 && exitStatus == QProcess::NormalExit) {
            emit setStatus("update successful");
        }
        else {
            emit setStatus("update failed");
        }

        QFile::remove(savePath);
        emit closeUpdater();
    });

    process->start("pkexec", arguments);
}

bool UpdaterLogic::calculateSha256(const QString &sha256, QFile &file) {
    emit setStatus("Calculating sha256");

    if (!file.open(QIODevice::ReadOnly)) {
        emit setStatus("Can't read file");
        emit closeUpdater();
        return false;
    }

    QCryptographicHash hash(QCryptographicHash::Sha256);

    while (!file.atEnd()) {
        hash.addData(file.read(1024 * 1024));
    }

    file.close();

    if (sha256.toLower() == hash.result().toHex().toLower()) {
        emit setStatus("Sha256 valid!");
        return true;
    }
    else {
        emit setStatus("Sha256 mismatch!");

        file.remove();
        emit closeUpdater();

        return false;
    }
}