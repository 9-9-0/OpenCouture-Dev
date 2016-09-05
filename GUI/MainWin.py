import sys
from PyQt4 import QtGui, QtCore

class MainWin(QtGui.QMainWindow):
    def __init__(self):
        super(MainWin, self).__init__()

        self.initUI()

    def initUI(self):
        self.statusBar().showMessage('Testing')
        self.setGeometry(100, 100, 400, 250)
        self.setWindowTitle('OpenCouture Lite')
        self.centerUI()

        self.show()
    
    def centerUI(self):
        frame = self.frameGeometry()
        center = QtGui.QDesktopWidget().availableGeometry().center()
        frame.moveCenter(center)
        self.move(frame.topLeft())

    # Eventually change this so the window appears IF there are scheduled/running tasks/unsaved profiles
    # Note: First argument ties the message box to the parent, MainWin (I think?)
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', "Are you sure you want to quit?", QtGui.QMessageBox.Yes | QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    instance = MainWin()
    sys.exit(app.exec_())
