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

        for i in range(0,Num_Panes):
            toAppend=addGuagePane(Num_Panes,Cw,Wh,tile[i],Dsource,Keys[i],unit,Min,Max,Rt)

        simplePane["panes"]=toAppend
        json_object=json.dumps(simplePane,indent=4)
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