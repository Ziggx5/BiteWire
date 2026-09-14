#include "updater.h"
#include <iostream>
#include <qstring.h>
#include <QDir>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>

UpdaterLogic::UpdaterLogic(QObject *parent) : QObject(parent) {

}

void UpdaterLogic::downloadUpdate(const QString &downloadUrl) {
    QUrl url(downloadUrl);

    QString fileName = QFileInfo(url.path()).fileName();
    QString savePath = QDir::tempPath() + "/" + fileName;

    QNetworkAccessManager *manager = new QNetworkAccessManager();

    QNetworkReply *reply = manager->get(QNetworkRequest(url));

    QObject::connect(reply, &QNetworkReply::downloadProgress, this, &UpdaterLogic::downloadProgress);

    QObject::connect(reply,  &QNetworkReply::finished, [reply, manager, savePath]() {
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