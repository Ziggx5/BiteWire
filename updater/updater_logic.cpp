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

            QStringList arguments;
            arguments << "dnf5" << "install" << "-y" << savePath;

            process->start("pkexec", arguments);
        }
        else if (savePath.endsWith(".deb")) {
            std::cout << "deb update" << std::endl;
        }
        else {
            std::cout << "update error" << std::endl;
            return;
        }
    }
    else {
        std::cout << "update error" << std::endl;
        return;
    }
}