#ifndef UPDATER_H
#define UPDATER_H

#include <QWidget>
#include <QObject>
#include <QVBoxLayout>
#include <QLabel>
#include <QProgressBar>
#include <QTimer>

class UpdaterUI : public QWidget {
public:
    UpdaterUI(const QString &currentVersion, const QString &latestVersion, QWidget *parent = nullptr);

    void setProgress(int percent, double receivedMB, double totalMB);
    void setStatus(bool success);
    void downloadFinished();

private:
    QProgressBar *progressBar;
    QVBoxLayout *layout;
    QLabel *updatingLabel;
    QLabel *statusLabel;
    QTimer *updateTimer;
    QLabel *totalDownloaded;
    QString downloadStatus = "Downloading";

    int dots = 0;

    void UpdateText();
};

class UpdaterLogic : public QObject {
    Q_OBJECT
public:
    UpdaterLogic(QObject *parent = nullptr);

    void downloadUpdate(const QString &downloadUrl, const QString &currentSystem, const QString &bitewirePath);

signals:
    void progressChanged(int percent, double receivedMB, double totalMB);
    void setStatus(bool success);
    void closeUpdater();
    void downloadFinished();

private:
    void downloadProgress(qint64 bytesReceived, qint64 bytesTotal);
    void updateApp(const QString &currentSystem, const QString &savePath, const QString &bitewirePath);
    void extractZip(const QString &savePath, const QString &unZipDirectory, const QString &appDirectory);
    void updateWindowsApp(const QString& unZipDirectory, const QString& appDirectory);
    void updateLinuxApp(const QStringList &arguments);
};

#endif