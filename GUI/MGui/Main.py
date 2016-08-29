from PyQt4 import QtGui
import sys
import OpenCouture

class Test(QtGui.QMainWindow, OpenCouture.Ui_MainWindow):
    def __init__(self, parent=None):
        super(Test, self).__init__(parent)
        self.setupUi(self)

def main():
    app = QtGui.QApplication(sys.argv)
    instance = Test()
    instance.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

