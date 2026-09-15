#include <iostream>
#include <QApplication>
#include <QVBoxLayout>
#include <QLabel>
#include <QWidget>
#include <QTimer>
#include "updater.h"
#include <QHBoxLayout>

UpdaterUI::UpdaterUI(const QString &currentVersion, const QString &latestVersion, QWidget *parent) : QWidget(parent) {
    resize(200, 250);
    setWindowFlag(Qt::FramelessWindowHint);
    setObjectName("updater");
    setStyleSheet("QWidget#updater {"
                    "background-color: qlineargradient("
                        "x1:0, y1:0, x2:1, y2:1,"
                        "stop:0 #0e1117,"
                        "stop:0.5 #151a22,"
                        "stop:1 #1a1f2b"
                    ")"
                 "};"
                );
    layout = new QVBoxLayout(this);

    QLabel *title =new QLabel("BiteWire");
    title->setStyleSheet("color: #e6edf3;"
                         "font-size: 28px;"
                         "font-weight: 600;"
                         "letter-spacing: 1px;");

    QLabel *line = new QLabel();
    line->setFixedSize(120, 2);
    line->setStyleSheet("background-color: #3b82f6; border-radius: 1px;");

    updatingLabel = new QLabel("Updating");
    updatingLabel->setStyleSheet("font-size: 12px;"
                                 "color: #a5a8ad;");

    progressBar = new QProgressBar();
    progressBar->setRange(0, 100);
    progressBar->setValue(0);
    progressBar->setFixedSize(80, 5);
    progressBar->setTextVisible(false);
    progressBar->setStyleSheet("QProgressBar { "
                                    "background-color: #1c1f26; "
                                    "border-radius: 1px;"
                                "}"

                               "QProgressBar::chunk { "
                                    "background-color: #3b82f6;"
                                    "border-radius: 2px;"
                                "}"
                              );

    QHBoxLayout * footerLayout = new QHBoxLayout();

    QLabel *versionLabel = new QLabel(currentVersion + " => " + latestVersion);
    versionLabel->setStyleSheet("color: #a5a8ad; font: 10px;");

    QLabel *creatorLabel = new QLabel("Created by Ziggx5");
    creatorLabel->setStyleSheet("color: #a5a8ad; font: 10px;");

    footerLayout->addWidget(versionLabel);
    footerLayout->addStretch();
    footerLayout->addWidget(creatorLabel);

    layout->addStretch();
    layout->addWidget(title, 0, Qt::AlignCenter);
    layout->addSpacing(10);
    layout->addWidget(line, 0, Qt::AlignCenter);
    layout->addSpacing(10);
    layout->addWidget(progressBar, 0, Qt::AlignCenter);
    layout->addWidget(updatingLabel, 0, Qt::AlignCenter);
    layout->addStretch();
    layout->addLayout(footerLayout);

    QTimer *timer = new QTimer(this);

    connect(timer, &QTimer::timeout, this, &UpdaterUI::UpdateText);
    timer->start(500);
};

void UpdaterUI::UpdateText() {
    dots++;

    if (dots > 3) {
        dots = 0;
    }

    updatingLabel->setText("Updating" + QString(dots, '.'));
}

void UpdaterUI::setProgress(int percent) {
    progressBar->setValue(percent);
    std::cout << std::to_string(percent) << std::endl;
}