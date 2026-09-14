#include <iostream>
#include <QApplication>
#include "updater.h"
#include <QCommandLineParser>
#include <QCommandLineOption>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QCommandLineParser parser;

    QCommandLineOption urlOption("url", "URL of the update file", "url");

    parser.addOption(urlOption);
    parser.process(app);

    QString downloadUrl = parser.value(urlOption);

    UpdaterLogic logic;

    UpdaterUI window;
    window.show();

    QObject::connect(&logic, &UpdaterLogic::progressChanged, &window, &UpdaterUI::setProgress);

    logic.downloadUpdate(downloadUrl);

    return app.exec();
}