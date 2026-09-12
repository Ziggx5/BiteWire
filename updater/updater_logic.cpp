#include "updater.h"
#include <iostream>
#include <qstring.h>
#include <QDir>
#include <QNetworkAccessManager>
#include <QNetworkReply>
#include <QNetworkRequest>

void downloadUpdate(const QString &downloadUrl) {
    QUrl url(downloadUrl);
    QString fileName = QFileInfo(url.path()).fileName();
    QString savePath = QDir::tempPath() + "/" + fileName;

    QNetworkAccessManager *manager = new QNetworkAccessManager();

    QNetworkReply *reply = manager->get(QNetworkRequest(url));

    QObject::connect(reply,  &QNetworkReply::finished, [reply, manager]() {
        std::cout << "download finished" << std::endl;

        if (reply->error() != QNetworkReply::NoError) {
            std::cout << "download error" << std::endl;

            reply->deleteLater();
            manager->deleteLater();
            return;
        }

        std::cout << "download byted" + std::to_string(reply->readAll().size()) << std::endl;

        reply->deleteLater();
        manager->deleteLater();
    }
    );
}