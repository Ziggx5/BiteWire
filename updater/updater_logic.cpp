#include "updater.h"
#include <iostream>
#include <qstring.h>
#include <QDir>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>
#include <QProcess>

UpdaterLogic::UpdaterLogic(QObject *parent) : QObject(parent) {

}

void UpdaterLogic::downloadUpdate(const QString &downloadUrl, const QString &currentSystem) {
    QUrl url(downloadUrl);

    QString fileName = QFileInfo(url.path()).fileName();
    QString savePath = QDir::tempPath() + "/" + fileName;

    QNetworkAccessManager *manager = new QNetworkAccessManager();

    QNetworkReply *reply = manager->get(QNetworkRequest(url));

    QObject::connect(reply, &QNetworkReply::downloadProgress, this, &UpdaterLogic::downloadProgress);

    QObject::connect(reply,  &QNetworkReply::finished, [reply, manager, savePath, this, currentSystem]() {
        std::cout << "download finished" << std::endl;

        if (reply->error() != QNetworkReply::NoError) {
            std::cout << "download error" << std::endl;

            reply->deleteLater();
            manager->deleteLater();
            return;
        }

        QFile file(savePath);

        if (!file.open(QIODevice::WriteOnly)) {
            std::cout << "file open error" << std::endl;

            reply->deleteLater();
            manager->deleteLater();
            return;
        }

        file.write(reply->readAll());
        file.close();

        std::cout << "download complete" << std::endl;

        updateApp(currentSystem, savePath);

        reply->deleteLater();
        manager->deleteLater();
    }
    );
}

void UpdaterLogic::downloadProgress(qint64 bytesReceived, qint64 bytesTotal) {
    if (bytesTotal <= 0)
        return;

    int percent = static_cast<int>(bytesReceived * 100 / bytesTotal);

    std::cout << "percent " << percent << "%" << std::endl;

    emit progressChanged(percent);
}

void UpdaterLogic::updateApp(const QString &currentSystem, const QString &savePath) {
    if (currentSystem == "windows") {
        std::cout << "windows update" << std::endl;
    }
    else if (currentSystem == "linux") {
        if (savePath.endsWith(".rpm")) {
            QProcess *process = new QProcess(this);

            QObject::connect(process, &QProcess::finished, process, &QProcess::deleteLater);
            QObject::connect(process, &QProcess::finished, [this](int exitCode, QProcess::ExitStatus exitStatus) {
                if (exitCode == 0) {
                    std::cout << "Update successful" << std::endl;
                    emit setStatus(true);
                    emit closeUpdater();
                }
                else {
                    std::cout << "Update failed" << std::endl;
                    emit setStatus(true);
                    emit closeUpdater();
                }
            });

            QStringList arguments;
            arguments << "dnf5" << "install" << "-y" << savePath;

            process->start("pkexec", arguments);
        }
        else if (savePath.endsWith(".deb")) {
            std::cout << "deb update" << std::endl;
            QProcess *process = new QProcess(this);

            QObject::connect(process, &QProcess::finished, process, &QProcess::deleteLater);
            QObject::connect(process, &QProcess::finished, [this](int exitCode, QProcess::ExitStatus exitStatus) {
                if (exitCode == 0) {
                    std::cout << "Update successful" << std::endl;
                    emit setStatus(true);
                    emit closeUpdater();
                }
                else {
                    std::cout << "Update failed" << std::endl;
                    emit setStatus(true);
                    emit closeUpdater();
                }
            });

            QStringList arguments;
            arguments << "apt" << "install" << "-y" << savePath;

            process->start("pkexec", arguments);
        }
        else {
            std::cout << "update error" << std::endl;
            emit closeUpdater();
            return;
        }
    }
    else {
        std::cout << "update error" << std::endl;
        emit closeUpdater();
        return;
    }
}