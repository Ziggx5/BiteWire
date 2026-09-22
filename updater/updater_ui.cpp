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

    statusLabel = new QLabel("Downloading");
    statusLabel->setStyleSheet("font-size: 12px;"
                                 "color: #a5a8ad;");

    totalDownloaded = new QLabel("0 / 0 MB");
    totalDownloaded->setStyleSheet(
        "color: #8b949e;"
        "font-size: 9px;"
    );

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
    layout->addWidget(totalDownloaded, 0, Qt::AlignCenter);
    layout->addWidget(statusLabel, 0, Qt::AlignCenter);
    layout->addStretch();
    layout->addLayout(footerLayout);

    updateTimer = new QTimer(this);

    connect(updateTimer, &QTimer::timeout, this, &UpdaterUI::UpdateText);
    updateTimer->start(500);
};

void UpdaterUI::UpdateText() {
    dots++;

    if (dots > 3) {
        dots = 0;
    }

    statusLabel->setText(downloadStatus + QString(dots, '.'));
}

void UpdaterUI::setProgress(int percent, double receivedMB, double totalMB) {
    progressBar->setValue(percent);
    totalDownloaded->setText(QString::number(receivedMB, 'f', 1) + " / " + QString::number(totalMB, 'f', 1) + " MB");
}

void UpdaterUI::setStatus(const QString &status) {
    updateTimer->stop();
    downloadStatus = status;
    statusLabel->setText(downloadStatus);
}

void UpdaterUI::downloadFinished() {
    updateTimer->stop();
    progressBar->hide();
    totalDownloaded->hide();
    downloadStatus = "Download completed";
}