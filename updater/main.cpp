#include <iostream>
#include <QApplication>
#include "updater.h"
#include <QCommandLineParser>
#include <QCommandLineOption>
#include <QTimer>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QCommandLineParser parser;

    QCommandLineOption urlOption("url", "URL of the update file", "url");
    QCommandLineOption currentVersionOption("current_version", "Current BiteWire version", "current_version");
    QCommandLineOption newVersionOption("new_version", "New BiteWire version", "new_version");
    QCommandLineOption currentSystemOption("system", "Current operating system", "system");

    parser.addOption(urlOption);
    parser.addOption(currentVersionOption);
    parser.addOption(newVersionOption);
    parser.addOption(currentSystemOption);
    parser.process(app);

    QString downloadUrl = parser.value(urlOption);
    QString currentVersion = parser.value(currentVersionOption);
    QString newVersion = parser.value(newVersionOption);
    QString currentSystem = parser.value(currentSystemOption);

    UpdaterLogic logic;

    UpdaterUI window(currentVersion, newVersion);
    window.show();

    QObject::connect(&logic, &UpdaterLogic::progressChanged, &window, &UpdaterUI::setProgress);
    QObject::connect(&logic, &UpdaterLogic::setStatus, &window, &UpdaterUI::setStatus);

    QTimer::singleShot(50 , [&logic, downloadUrl, currentSystem]() {
        logic.downloadUpdate(downloadUrl, currentSystem);
    });

    return app.exec();
}