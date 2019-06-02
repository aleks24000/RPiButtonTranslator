import sys
from PyQt5 import QtWidgets
from RecUI import Ui_MainWindow
from RPiFunctions import start, stop_rec, upload_file
from gpiozero import Button
from signal import pause
from RPiFunctions import start_rec
from RPiFunctions import stop_rec
from RPiFunctions import upload_file

def startGui(Ui_MainWindow):
    Ui_MainWindow.pushButton.setStyleSheet("background-color: red")
    start(False)

def stopGui(Ui_MainWindow):
    stop_rec(False)
    Ui_MainWindow.pushButton.setStyleSheet("background-color: green")

def uploadGui(Ui_MainWindow):
    Ui_MainWindow.pushButton3.setStyleSheet("background-color: red")
    upload_file()
    Ui_MainWindow.pushButton3.setStyleSheet("background-color: green")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    ex = Ui_MainWindow()
    w = QtWidgets.QMainWindow()
    ex.setupUi(w)

    button = Button(12)
    button_stop = Button(20)
    button_upload = Button(26)

    button.when_pressed = startGui(ex)
    button_stop.when_pressed = stopGui(ex)
    button_upload.when_pressed = uploadGui(ex)

    w.show()
    #startGui(ex)
    #ex.pushButton.setStyleSheet("background-color: red")
    sys.exit(app.exec_())
    #app.exec_()
    print("exiting")