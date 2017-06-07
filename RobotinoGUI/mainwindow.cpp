#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    QString DOCKER_HOST = "tcp://10.2.1.11:2375";
    ui->textBrowser->setText(DOCKER_HOST);
    QString IP_add = "";
}

MainWindow::~MainWindow()
{
    //delete ui;
}

void MainWindow::on_pushButton_clicked()
{
    QString DOCKER_HOST = "tcp://10.2.1.11:2375";
    QString IP_add ="";
    IP_add = QInputDialog::getText(this, tr("QInputDialog::getText()"),tr("IPADD:"), QLineEdit::Normal);
    QString ip_path = "docker -H tcp://" +IP_add + ":2375 images";
    QProcess process;
    //process.start("gnome-terminal ");
    //process.waitForStarted(1000);
    //process.execute("docker -H tcp://10.2.1.11:2375 ps -a");//docker /s -H tcp://10.2.1.11:2375 ps
    process.start(ip_path);
    //QProcess::execute("docker -H tcp://10.2.1.11:2375 ps -a");
    process.waitForFinished();
    //process.start("gnome-terminal");
    //process.waitForStarted();
    QByteArray ba = process.readAll();
    //process.close();
    //process.read(4);
    //ui->textBrowser->append(process.read(4));
    ui->textBrowser->append(ba);
    //process.waitForFinished(50000);
}

void MainWindow::on_pushButton_2_clicked()
{
    QProcess *process = new QProcess ;
    QString DockerImg = "";
    DockerImg = QInputDialog::getText(this, tr("QInputDialog::getText()"),tr("Enter Docker Image Name:"), QLineEdit::Normal);
    //process.start("docker -H tcp://10.2.1.11:2375 run hello-world");//, QStringList() << "cd");
    process->start("gnome-terminal");
    process->waitForStarted();
    //docker -H tcp://10.2.1.11:2375 run hello-world");
    process->execute("docker -H tcp://10.2.1.11:2375 run -it --rm docker_robotino_node");
    //connect(process &QProcess::readyRead, this);

}
