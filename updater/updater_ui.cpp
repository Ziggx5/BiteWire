#include <QApplication>
#include <QVBoxLayout>
#include <QLabel>
#include <QWidget>
#include <QTimer>

class UpdaterUI : public QWidget {
public:
    UpdaterUI() {
        setWindowTitle("Updater");
        resize(200, 250);
        setWindowFlags(Qt::FramelessWindowHint);
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

        updating_label = new QLabel("Updating");
        updating_label->setStyleSheet("font-size: 12px;"
                                      "color: #a5a8ad;");

        QHBoxLayout * footer_layout = new QHBoxLayout();

        QLabel *version_label = new QLabel("version => version");
        version_label->setStyleSheet("color: #a5a8ad; font: 10px;");

        QLabel *creator_label = new QLabel("Created by Ziggx5");
        creator_label->setStyleSheet("color: #a5a8ad; font: 10px;");

        footer_layout->addWidget(version_label);
        footer_layout->addStretch();
        footer_layout->addWidget(creator_label);

        layout->addStretch();
        layout->addWidget(title, 0, Qt::AlignCenter);
        layout->addSpacing(10);
        layout->addWidget(line, 0, Qt::AlignCenter);
        layout->addSpacing(10);
        layout->addWidget(updating_label, 0, Qt::AlignCenter);
        layout->addStretch();
        layout->addLayout(footer_layout);

        QTimer *timer = new QTimer(this);

        connect(timer, &QTimer::timeout, this, &UpdaterUI::UpdateText);
        timer->start(500);
    }

private:
    QVBoxLayout * layout;
    QLabel * updating_label;
    int dots = 0;

    void UpdateText() {
        dots++;

        if (dots > 3) {
            dots = 0;
        }

        updating_label->setText("Updating" + QString(dots, '.'));
    }
};

int main(int argc, char *argv[]) {
    QApplication app(argc, argv);

    UpdaterUI window;
    window.show();

    return app.exec();
}