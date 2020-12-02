from PyQt5.QtWidgets import * 
from PyQt5 import QtCore 
from PyQt5 import QtGui 
import json
import sys

simplePane={
	"version": 1,
	"allow_edit": True,
	"plugins": [],
	"panes": "",
	"datasources": [],
	"columns": 5,
	"lastUpdateTime": 1606289011190,
	"theme": "blue"
}

def mqtt(n,sn,p):
    MQTT = {
    "name": n,
    "type": "mqttdatasource2",
    "settings": {
      "server": sn,
      "port": p,
      "client_id": "",
      "username": "",
      "password": "",
      "topics_table": []
    }
  }
    return(MQTT)

def topicsList(key,topic):
    TopicsList={
            "key": key,
            "topic": topic,
            "is_JSON": "false"
            }
    return TopicsList

def addPane(value,column_width):
	p=[]
	pane={
	"width": 2,
	"row": {
	    "9": 1
		},
	"col": {
	    "9": 1
		},
	"col_width": column_width,
	    "widgets": []
		}
	for i in range(0,value):
		p.append(pane)
	return p

def addGuagePane(value,column_width,widgetHeight,Title,Dsource,key,unit,min,max,refreshTime):
	GuagePane={
				"width": 2,
				"row": {
					"9": 1
				},
				"col": {
					"9": 1
				},
				"col_width": column_width,
				"widgets": [
					{
						"type": "gauge",
						"settings": {
							"blocks": widgetHeight,
							"title": Title,
							"value": "datasources[\""+Dsource+"\"][\""+key+"\"]",
							"units": unit,
							"min_value": min,
							"max_value": max,
							"refreshtime": refreshTime,
							"percentages": "False",
							"pointer": "False"
						}
					}
				]
			}
	return GuagePane
	
def MainJson_Update(name):
	mainJson_update={
				"display_name": name,
				"dashboard_file": "/boards/"+name+".json",
				"icon": "fa-file-image-o",
				"role": "1"
			}
	return(mainJson_update)

class baseWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(QtGui.QIcon('C:/Users/Ajay Sharma/Desktop/dashboard_py/icon.jpg')) 

        self.title = "Create Dashboard"
        self.top = 100
        self.left = 100
        self.width = 680
        self.height = 500

        self.pushButton = QPushButton("Emp_Panes", self)
        self.pushButton.move(50, 50)
        self.pushButton.setToolTip("<h3>You can create dashboard with multiple empty pane</h3>")

        self.pushButton.clicked.connect(self.EmpPane)

        self.pushButton2 = QPushButton("Guage", self)
        self.pushButton2.move(50, 100)
        self.pushButton2.setToolTip("<h3>You can create dashboard with multiple Guage Widget pane</h3>")

        self.pushButton2.clicked.connect(self.GuagePane)

        self.pushButton3 = QPushButton("MQTT", self)
        self.pushButton3.move(50, 150)
        self.pushButton3.setToolTip("<h3>You can create dashboard with multiple Guage Widget pane</h3>")

        self.pushButton3.clicked.connect(self.DatasourceWindow) 

        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)
        self.show()

    def EmpPane(self):                                             
        self.w = Window()
        self.w.show()
        self.hide()

    def GuagePane(self):                                             
        self.w = GuageWindow()
        self.w.show()
        self.hide()
    
    def DatasourceWindow(self):                                             
        self.w = DsourceWindow()
        self.w.show()
        self.hide()


class Window(QDialog): 
  
    # constructor 
    def __init__(self): 
        super(Window, self).__init__() 

        #setting Icon to window
        self.setWindowIcon(QtGui.QIcon('C:/Users/Ajay Sharma/Desktop/dashboard_py/icon.jpg')) 
  
        # setting window title 
        self.setWindowTitle("Embedos") 
  
        # setting geometry to the window 
        self.setGeometry(100, 200, 800, 600)
  
        # creating a group box 
        self.formGroupBox = QGroupBox("Create Empty Panes") 
  
        # creating spin box to select pane column_width  
        self.column_width = QSpinBox()
  
        # creating spin box to select number of Panes 
        self.Panes = QSpinBox() 
  
        # creating a line edit 
        self.nameLineEdit = QLineEdit() 
  
        # calling the method that create the form 
        self.createForm() 
  
        # creating a dialog button for ok and cancel 
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.pushButton = QPushButton("BACK_2_HOME", self)

        self.pushButton.clicked.connect(self.home)

        self.pushButton.move(275, 200)
          
        # adding action when form is accepted 
        self.buttonBox.accepted.connect(self.generate) 
  
        # addding action when form is rejected 
        self.buttonBox.rejected.connect(self.home)
  
        # creating a vertical layout 
        mainLayout = QVBoxLayout() 
  
        # adding form group box to the layout 
        mainLayout.addWidget(self.formGroupBox) 
  
        # adding button box to the layout 
        mainLayout.addWidget(self.buttonBox)

        mainLayout.addWidget(self.pushButton)
  
        # setting lay out 
        self.setLayout(mainLayout)
        self.show()

    def home(self):                                             
        self.w = baseWindow()
        self.w.show()
        self.hide()
    
    def notifyError(self, notice, message):
        self.popUp=QMessageBox.critical(self, notice, message, QMessageBox.Ok)
    def notifySuccess(self, notice, message):
        self.popUp=QMessageBox.information(self, notice, message, QMessageBox.Ok)


    def alert(self):
            self.popUp=QMessageBox.warning(self, "Warning", "DASHBOARD ALREADY EXIST WANT TO UPDATE",QMessageBox.Yes | QMessageBox.No)           
            # if self.popUp==QMessageBox.No:
            #     self.event.ignore()
            return(self.popUp==QMessageBox.Yes)

    # get generate method called when form is accepted
    def generate(self):
        allow=True
        both=True
        # storing the form information 
        name = self.nameLineEdit.text()
        Num_Panes = int(self.Panes.text())
        cW = int(self.column_width.text())
        if name=="":
            self.notifyError('ERROR','ENTER A VALID DASHBOARD NAME')
            allow=False
        
        if allow==True:
            #reading main.json file
            with open('C:/Users/Ajay Sharma/Desktop/embedos/demodashboard/public/boards/main.json','r') as f1:
                data = json.load(f1)
            boards=data["dashboards"]

            #checking if the dashboard already exists
            for dict in boards:
                for key,value in dict.items():
                    if value==name:
                            update=self.alert()
                            if update==True:
                                both=False
                                simplePane["panes"]=addPane(Num_Panes,cW)
                                json_object=json.dumps(simplePane, indent = 4)
                                with open('C:/Users/Ajay Sharma/Desktop/embedos/demodashboard/public/boards/'+name+'.json','w') as f:
                                    f.write(json_object)
                                self.notifySuccess('SUCCESS',name+' UPDATED SUCCESSFULLY')
                            else:
                                return None
                                

            if both==True:
                #preparing data to update main.json
                data["dashboards"].append(MainJson_Update(name))

                #updating main.json
                with open('C:/Users/Ajay Sharma/Desktop/embedos/demodashboard/public/boards/main.json','w') as f2:
                    json_object2=json.dumps(data, indent = 4)
                    f2.write(json_object2)
                
                #preparing data to create dashboard.json files
                simplePane["panes"]=addPane(Num_Panes,cW)
                json_object=json.dumps(simplePane, indent = 4)

                #creating dashboard.json files
                with open('C:/Users/Ajay Sharma/Desktop/embedos/demodashboard/public/boards/'+name+'.json','w') as f:
                    f.write(json_object)
                self.notifySuccess('SUCCESS',name+' CREATED SUCCESSFULLY')
    
        # closing the window  
  
    # creat form method 
    def createForm(self): 
  
        # creating a form layout 
        layout = QFormLayout() 
  
        # adding rows 
        # for name and adding input text 
        layout.addRow(QLabel("Dashboard Name"), self.nameLineEdit) 
  
        # for degree and adding combo box 
        layout.addRow(QLabel("Number of Panes"), self.Panes) 
  
        # for age and adding spin box 
        layout.addRow(QLabel("Colum Width for each pane"), self.column_width) 
  
        # setting layout 
        self.formGroupBox.setLayout(layout)

class GuageWindow(QDialog): 
  
    # constructor 
    def __init__(self): 
        super(GuageWindow, self).__init__() 

        #setting Icon to window
        self.setWindowIcon(QtGui.QIcon('C:/Users/Ajay Sharma/Desktop/dashboard_py/icon.jpg')) 
  
        # setting window title 
        self.setWindowTitle("Embedos") 
  
        # setting geometry to the window 
        self.setGeometry(100, 200, 800, 600)
  
        # creating a group box 
        self.formGroupBox = QGroupBox("Create DashBoard")
 
        self.DashName = QLineEdit()

        self.Title = QLineEdit()

        self.DataSource = QLineEdit()

        self.Keys = QLineEdit()

        self.Unit = QLineEdit()
  
        # creating a line edit 
        self.Npanes = QSpinBox()

        self.ColWidthpanes = QSpinBox()

        self.WidgetHeight = QSpinBox()

        self.MinValue = QSpinBox()

        self.MaxValue = QSpinBox()

        self.RefreshTime = QSpinBox()

        self.Npanes.setRange(0,100)
        self.ColWidthpanes.setRange(1,10)
        self.WidgetHeight.setRange(1,10)
        self.MinValue.setRange(-1000,0)
        self.MaxValue.setRange(0,1000)
        self.RefreshTime.setRange(0,1000)


  
        # calling the method that create the form 
        self.createForm() 
  
        # creating a dialog button for ok and cancel 
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.pushButton = QPushButton("BACK_2_HOME", self)

        self.pushButton.clicked.connect(self.home)

        self.pushButton.move(275, 200)
          
        # adding action when form is accepted 
        self.buttonBox.accepted.connect(self.generate2) 
  
        # addding action when form is rejected 
        self.buttonBox.rejected.connect(self.home)
  
        # creating a vertical layout 
        mainLayout = QVBoxLayout() 
  
        # adding form group box to the layout 
        mainLayout.addWidget(self.formGroupBox) 
  
        # adding button box to the layout 
        mainLayout.addWidget(self.buttonBox)

        mainLayout.addWidget(self.pushButton)
  
        # setting lay out 
        self.setLayout(mainLayout)
        self.show()

    def home(self):                                             
        self.w = baseWindow()
        self.w.show()
        self.hide()
    
    def notifyError(self, notice, message):
        self.popUp=QMessageBox.critical(self, notice, message, QMessageBox.Ok)
    def notifySuccess(self, notice, message):
        self.popUp=QMessageBox.information(self, notice, message, QMessageBox.Ok)


    def alert(self):
            self.popUp=QMessageBox.warning(self, "Warning", "DASHBOARD ALREADY EXIST WANT TO UPDATE",QMessageBox.Yes | QMessageBox.No)           
            # if self.popUp==QMessageBox.No:
            #     self.event.ignore()
            return(self.popUp==QMessageBox.Yes)

    def generate2(self):
        name = self.DashName.text()
        Title = self.Title.text()
        Title = Title.split(',')
        unit = self.Unit.text()
        Dsource = self.DataSource.text()
        Keys = self.Keys.text()
        Keys = Keys.split(',')

        Num_Panes = int(self.Npanes.text())
        Cw = int(self.ColWidthpanes.text())
        Wh = int(self.WidgetHeight.text())
        Min = int(self.MinValue.text())
        Max = int(self.MaxValue.text())
        Rt = int(self.RefreshTime.text())

        toAppend=[]

        for i in range(0,Num_Panes):
            toAppend.append(addGuagePane(Num_Panes,Cw,Wh,Title[i],Dsource,Keys[i],unit,Min,Max,Rt))

        simplePane["panes"]=toAppend
        json_object=json.dumps(simplePane,indent=4)
        print(json_object)
        with open('C:/Users/Ajay Sharma/Desktop/embedos/demodashboard/public/boards/'+name+'.json','w') as f:
            f.write(json_object)

        with open('C:/Users/Ajay Sharma/Desktop/embedos/demodashboard/public/boards/main.json','r') as f1:
            data = json.load(f1)
        boards=data["dashboards"]

        data["dashboards"].append(MainJson_Update(name))

        #updating main.json
        with open('C:/Users/Ajay Sharma/Desktop/embedos/demodashboard/public/boards/main.json','w') as f2:
            json_object2=json.dumps(data, indent = 4)
            f2.write(json_object2)
        
        self.notifySuccess('SUCCESS',name+' CREATED SUCCESSFULLY')
    # get generate method called when form is accepted
  
    # creat form method 
    def createForm(self): 
  
        # creating a form layout 
        layout = QFormLayout() 
  
        # adding rows 
        # for name and adding input text 
        layout.addRow(QLabel("Dashboard Name"), self.DashName) 
        layout.addRow(QLabel("Widget Title"), self.Title) 
        layout.addRow(QLabel("Unit of measure"), self.Unit) 
        layout.addRow(QLabel("Data Source Name"), self.DataSource) 
        layout.addRow(QLabel("Enter Keys"), self.Keys)

        layout.addRow(QLabel("Number of Panes"), self.Npanes) 
        layout.addRow(QLabel("Colum Width for each pane"), self.ColWidthpanes) 
        layout.addRow(QLabel("Height of Widget"), self.WidgetHeight) 
        layout.addRow(QLabel("Minimum Value"), self.MinValue) 
        layout.addRow(QLabel("Maximum Value"), self.MaxValue) 
        layout.addRow(QLabel("RefreshTime"), self.RefreshTime) 
  
        # setting layout 
        self.formGroupBox.setLayout(layout)

class DsourceWindow(QDialog): 
  
    # constructor 
    def __init__(self): 
        super(DsourceWindow, self).__init__() 

        #setting Icon to window
        self.setWindowIcon(QtGui.QIcon('C:/Users/Ajay Sharma/Desktop/dashboard_py/icon.jpg')) 
  
        # setting window title 
        self.setWindowTitle("Embedos") 
  
        # setting geometry to the window 
        self.setGeometry(100, 200, 800, 600)
  
        # creating a group box 
        self.formGroupBox = QGroupBox("Create Datasource")

        self.Number = QSpinBox()
 
        self.DsourceName = QLineEdit()

        self.ServerName = QLineEdit()

        self.PortNumber = QLineEdit()

        self.keys = QLineEdit()

        self.Topics = QLineEdit()
  
        # calling the method that create the form 
        self.createForm() 
  
        # creating a dialog button for ok and cancel 
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.pushButton = QPushButton("BACK_2_HOME", self)

        self.pushButton.clicked.connect(self.home)

        self.pushButton.move(275, 200)
          
        # adding action when form is accepted 
        self.buttonBox.accepted.connect(self.generate3) 
  
        # addding action when form is rejected 
        self.buttonBox.rejected.connect(self.home)
  
        # creating a vertical layout 
        mainLayout = QVBoxLayout() 
  
        # adding form group box to the layout 
        mainLayout.addWidget(self.formGroupBox) 
  
        # adding button box to the layout 
        mainLayout.addWidget(self.buttonBox)

        mainLayout.addWidget(self.pushButton)
  
        # setting lay out 
        self.setLayout(mainLayout)
        self.show()

    def home(self):                                             
        self.w = baseWindow()
        self.w.show()
        self.hide()
    
    def notifyError(self, notice, message):
        self.popUp=QMessageBox.critical(self, notice, message, QMessageBox.Ok)
    def notifySuccess(self, notice, message):
        self.popUp=QMessageBox.information(self, notice, message, QMessageBox.Ok)


    def alert(self):
            self.popUp=QMessageBox.warning(self, "Warning", "DASHBOARD ALREADY EXIST WANT TO UPDATE",QMessageBox.Yes | QMessageBox.No)           
            # if self.popUp==QMessageBox.No:
            #     self.event.ignore()
            return(self.popUp==QMessageBox.Yes)

    def generate3(self):

        num=int(self.Number.text())

        name=self.DsourceName.text()

        Sname=self.ServerName.text()

        Pnum=self.PortNumber.text()

        keys=self.keys.text()
        k=keys.split(',')

        topics=self.Topics.text()
        t=topics.split(',')

        toAppend=mqtt(name,Sname,Pnum)

        TopicsAppend=[]
        for i in range(0,num):
            TopicsAppend.append(topicsList(k[i],t[i]))

        toAppend['settings']['topics_table']=TopicsAppend


        with open('C:/Users/Ajay Sharma/Desktop/embedos/demodashboard/public/datasource/ds.json','r') as f1:
            data = json.load(f1)
        data.append(toAppend)

        with open('C:/Users/Ajay Sharma/Desktop/embedos/demodashboard/public/datasource/ds.json','w') as f2:
            json_object2=json.dumps(data, indent = 4)
            f2.write(json_object2)
        
        self.notifySuccess('SUCCESS',name+' DATA_SOURCE CREATED SUCCESSFULLY')
    # get generate method called when form is accepted
  
    # creat form method 
    def createForm(self): 
  
        # creating a form layout 
        layout = QFormLayout() 
  
        # adding rows 
        # for name and adding input text 
        layout.addRow(QLabel("number"), self.Number) 
        layout.addRow(QLabel("data source name"), self.DsourceName) 
        layout.addRow(QLabel("server name"), self.ServerName) 
        layout.addRow(QLabel("port"), self.PortNumber)
        layout.addRow(QLabel("keys"), self.keys)
        layout.addRow(QLabel("topic"), self.Topics)
  
        # setting layout 
        self.formGroupBox.setLayout(layout)
