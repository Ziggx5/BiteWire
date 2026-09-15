#ifndef UPDATER_H
#define UPDATER_H

#include <QWidget>
#include <QObject>
#include <QVBoxLayout>
#include <QLabel>
#include <QProgressBar>

class UpdaterUI : public QWidget {
public:
    UpdaterUI(const QString &currentVersion, const QString &latestVersion, QWidget *parent = nullptr);

    void setProgress(int percent);

private:
    QProgressBar *progressBar;
    QVBoxLayout *layout;
    QLabel *updatingLabel;

    int dots = 0;

    void UpdateText();
};

class UpdaterLogic : public QObject {
    Q_OBJECT
public:
    UpdaterLogic(QObject *parent = nullptr);

    void downloadUpdate(const QString &downloadUrl, const QString &currentSystem);

signals:
    void progressChanged(int percent);

private:
    void downloadProgress(qint64 bytesReceived, qint64 bytesTotal);
    void updateApp(const QString &currentSystem, const QString &savePath);
};

#endif