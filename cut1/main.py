from PyQt5 import QtWidgets
from helloWorld import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog, QApplication
from cut import videoCut
import sys
from PyQt5.QtCore import *

class MyWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setupUi(self)
        self.ini_path = ''

    def read(self):
        self.ini_path, ok = QFileDialog.getOpenFileName(self, 'select file', '/home')
        if ok:
            self.textBrowser.append(self.ini_path)
            self.textBrowser.append("Loaded Successfully...")

    def start(self):
        self.textBrowser.append("already start")
        if self.ini_path == '':
            self.textBrowser.append("You need to select a ini file")
        else:
            self.textBrowser.append("Cutting, please wait")
            QApplication.processEvents()
            videoCut(self, self.ini_path)
            QApplication.processEvents()
            self.textBrowser.append("Done!")

class WorkThread(QThread):
    trigger = pyqtSignal()

    def __int__(self):
        super(WorkThread, self).__init__()

    def run(self):
        for i in range(2000000000):
            pass

        # 循环完毕后发出信号
        self.trigger.emit()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    myshow = MyWindow()
    myshow.show()
    sys.exit(app.exec_())