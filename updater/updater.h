#ifndef UPDATER_H
#define UPDATER_H

#include <QWidget>
#include <QVBoxLayout>
#include <QLabel>

class UpdaterUI : public QWidget {
public:
    UpdaterUI(const QString &downloadUrl, QWidget *parent = nullptr);

private:
    QVBoxLayout *layout;
    QLabel *updatingLabel;

    int dots = 0;

    void UpdateText();
};

void downloadUpdate(const QString &downloadUrl);

#endif