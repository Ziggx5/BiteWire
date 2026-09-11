#include <iostream>
#include <ostream>
#include <QApplication>
#include "updater.h"
#include <QCommandLineParser>
#include <QCommandLineOption>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QCommandLineParser parser;

    QCommandLineOption url_option("url", "URL of the update file", "url");

    parser.addOption(url_option);
    parser.process(app);

    QString download_url = parser.value(url_option);

    UpdaterUI window;
    window.show();

    std::cout << download_url.toStdString() << std::endl;

    return app.exec();
}