from PyQt5.QtWidgets import * 
from PyQt5 import QtCore 
from PyQt5 import QtGui 
import json
import sys
from DashGenerator2 import*
  
# main method 
if __name__ == '__main__': 
  
    # create pyqt5 app 
    app = QApplication(sys.argv)
  
    # create the instance of our Window 
    window = baseWindow() 
  
    # start the app 
    sys.exit(app.exec()) 
