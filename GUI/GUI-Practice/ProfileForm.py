## TO DO ###
# [/] Add in input boxes and corresponding labels
# [X] Connect this with CreateProfile.py
# [ ] Clean up the module dependency structure
# [ ] Implement QSplitter and look at style keys

from PyQt4 import QtGui, QtCore
from Stage import CreateProfile


class ProfileWindow(QtGui.QWidget):
    def __init__(self):
        super(ProfileWindow, self).__init__()
        
        #Setup UI
        self.width = 900
        self.height= 450
        self.setUI()

        #Stage Folders? Possibly leave this to installer
        ###
        #

        #Create base profile
        self.baseProfile = CreateProfile.UserProfile()

    def setUI(self):
        # Set Essentials #
        self.setWindowTitle('OpenCouture - Profiles')
        self.setGeometry(0, 0, self.width, self.height)
        self.setWindowIcon(QtGui.QIcon('Icon.png'))

        # Set Labels and Input Boxes #
        # NOTE: Decide on scope of labels and input boxes, how will they persist for multiple profiles...? Need to choose a data structure
        box_1_layout = QtGui.QFormLayout()
        #self.lbl_first_name = QtGui.QLabel(self)
        #self.lbl_first_name.move(25, 50)
        #self.lbl_first_name.setText("First Name")
        self.qle_first_name = QtGui.QLineEdit(self)
        box_1_layout.addRow("First Name", self.qle_first_name)
        #lbl_first_name = QtGui.QLabel(self)
        #lbl_first_name.move(60, 40)
        #lbl_first_name.setText("First Name")

        #self.lbl_last_name = QtGui.QLabel(self)
        #self.lbl_last_name.move(25, 75)
        #self.lbl_last_name.setText("Last Name")
        #self.lbl_email_address = QtGui.QLabel(self)
        #self.lbl_email_address.move(25, 100)
        #self.lbl_email_address.setText("Email Address")

        self.setLayout(box_1_layout)
        self.center()
        self.show()

    def center(self):
        frame = self.frameGeometry()
        centerPoint = QtGui.QDesktopWidget().availableGeometry().center()
        frame.moveCenter(centerPoint)
        self.move(frame.topLeft())
        #self.move(frame.topRight())

def main():
    import sys
    app = QtGui.QApplication(sys.argv)
    mainWindow = ProfileWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
