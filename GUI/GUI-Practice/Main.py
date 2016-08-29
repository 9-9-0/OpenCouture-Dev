import sys
from PyQt4 import QtGui, QtCore

class appWindow(QtGui.QMainWindow):
    def __init__(self):
        super(appWindow, self).__init__() # Figure out why AppWindow and self are both being passed to super()
        self.setGeometry(50, 50, 800, 500)
        self.setWindowTitle("OpenCouture")
        self.setWindowIcon(QtGui.QIcon('Icon.png'))

    ### MENU ACTIONS ###
        File_Quit = QtGui.QAction("&Quit Application", self)
        File_Quit.setShortcut("Ctrl+Q")
        File_Quit.setStatusTip('Exit the App')
        File_Quit.triggered.connect(self.exitApp)

    ### MENU CONFIGURATION ###
        self.statusBar()
        Menu_Main = self.menuBar()
        SubMenu_File = Menu_Main.addMenu('&File')
        SubMenu_File.addAction(File_Quit)
        
        self.home()       
             
        
    ### PAGES (Eventually modularize these? Include them in another file?) ###
    def home(self):
        btn_quit = QtGui.QPushButton("Quit", self)
        btn_quit.clicked.connect(self.exitApp)
        btn_quit.resize(100, 50)
        #btn_quit.resize(btn_quit.sizeHint())
        btn_quit.move(700, 450)
        self.show()
    
#   def profiles():

    ### CUSTOM APPLICATION ACTIONS ###
    def exitApp(self):
        #Add in checks for unsaved profiles, current running processes before exit
        sys.exit()

##############
#### MAIN ####
##############

def runProg():
    app = QtGui.QApplication(sys.argv)
    GUI = appWindow()
    sys.exit(app.exec_())

runProg();
