#include <iostream>
#include <QApplication>
#include "updater.h"
#include <QCommandLineParser>
#include <QCommandLineOption>
#include <QProcess>
#include <QTimer>

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    QCommandLineParser parser;

    QCommandLineOption urlOption("url", "URL of the update file", "url");
    QCommandLineOption currentVersionOption("current_version", "Current BiteWire version", "current_version");
    QCommandLineOption newVersionOption("new_version", "New BiteWire version", "new_version");
    QCommandLineOption currentSystemOption("system", "Current operating system", "system");
    QCommandLineOption bitewirePathOption("bitewire_path", "BiteWire Path", "bitewire_path");
    QCommandLineOption qtLibraryPathOption("qt_library_path", "BiteWire Library path", "qt_library_path");
    QCommandLineOption qtPluginPathOption("qt_plugin_path", "BiteWire plugin path", "qt_plugin_path");

    parser.addOption(urlOption);
    parser.addOption(currentVersionOption);
    parser.addOption(newVersionOption);
    parser.addOption(currentSystemOption);
    parser.addOption(bitewirePathOption);
    parser.addOption(qtLibraryPathOption);
    parser.addOption(qtPluginPathOption);
    parser.process(app);

    QString downloadUrl = parser.value(urlOption);
    QString currentVersion = parser.value(currentVersionOption);
    QString newVersion = parser.value(newVersionOption);
    QString currentSystem = parser.value(currentSystemOption);
    QString bitewirePath = parser.value(bitewirePathOption);
    QString qtLibraryPath = parser.value(qtLibraryPathOption);
    QString qtPluginPath = parser.value(qtPluginPathOption);

    UpdaterLogic logic;

    UpdaterUI window(currentVersion, newVersion);
    window.show();

    QProcessEnvironment env = QProcessEnvironment::systemEnvironment();

    env.insert("LD_LIBRARY_PATH", qtLibraryPath);
    env.insert("QT_PLUGIN_PATH", qtPluginPath);

    QObject::connect(&logic, &UpdaterLogic::progressChanged, &window, &UpdaterUI::setProgress);
    QObject::connect(&logic, &UpdaterLogic::setStatus, &window, &UpdaterUI::setStatus);
    QObject::connect(&logic, &UpdaterLogic::closeUpdater, [&window, bitewirePath, env, &app]() {
        QTimer::singleShot(2000, [&window, &app, bitewirePath, env]() {
            window.hide();

            QProcess process;
            process.setProcessEnvironment(env);
            process.setProgram(bitewirePath);

            process.startDetached();

            QTimer::singleShot(4000, &app, QApplication::quit);
        });
    });

    QTimer::singleShot(50 , [&logic, downloadUrl, currentSystem, bitewirePath]() {
        logic.downloadUpdate(downloadUrl, currentSystem, bitewirePath);
    });

    return app.exec();
}