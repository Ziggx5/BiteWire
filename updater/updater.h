#ifndef UPDATER_H
#define UPDATER_H

#include <QWidget>
#include <QVBoxLayout>
#include <QLabel>

class UpdaterUI : public QWidget {
public:
    UpdaterUI(QWidget *parent = nullptr);

private:
    QVBoxLayout *layout;
    QLabel *updating_label;

    int dots = 0;

    void UpdateText();
};

void UpdateApp();

#endif