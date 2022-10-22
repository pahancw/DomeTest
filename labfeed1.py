import sys
from PyQt5.QtWidgets import QDialog, QApplication,QMainWindow,QMessageBox
 
class labfeed1(QDialog):
	def __init__(self,username,uid):
		super().__init__()
		self.ui = Ui_labfeed()
		self.ui.setupUi(self)
		self.show()
		self.user = username
		self.uid = uid
		self.ui.label_welcome.setText("Logged in as " + self.user)
		self.ui.pushButton_submit.clicked.connect(self.submit)
		self.ui.pushButton_exit.clicked.connect(self.close)
		self.ui.checkBox_Consume.stateChanged.connect(self.consumenable)


	def submit(self):
		info = QMessageBox()
		info.setWindowTitle("Confirmation")
		info.setText("You are about to submit the apparatus information to the database!, Please click cancel if you are not sure!")
		info.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
		response = info.exec()

		if response == QMessageBox.Ok:
			lab = self.ui.comboBox_setlab.currentText()
			appid = self.ui.label_aid.text()
			appname = self.ui.lineEdit_Aname.text()
			condition = self.ui.comboBox_condition.currentText()
			use = self.ui.comboBox_use.currentText()
			consumables = self.ui.lineEdit_Consume.text()
			description = self.ui.textEdit_description.toPlainText()
			specifications = self.ui.textEdit_specs.toPlainText()
			qty = self.ui.spinBox_qty.value()
			uid = self.uid
			username =self.user
		
			if lab == "Thermodynamics Lab":
				setcollection = "Thermolab"
			elif lab == "Aero Lab":
				setcollection ="aerolab"
			elif lab == "Control systems Lab":
				setcollection ="control"
			elif lab == "Energy Lab":
				setcollection ="energy"
			elif lab == "Mechatronics Lab":
				setcollection ="mechatronics"
			else:
				info = QMessageBox()
				info.setWindowTitle("Apparatus registration")
				info.setText("Not available at the moment")
				info.exec_()
				self.hide()


			
			db = cluster["domelabs"]
			collection = db[setcollection]
			appidnum = collection.count_documents({}) + 1
			appid = setcollection + str(appidnum)

			self.ui.label_aid.setText(appid)
			post = {"_id": appid, "aname": appname, "condition":condition, "use":use, "consumables":consumables, "description":description, "specifications":specifications, "quantity": qty, "addedby": uid}
			collection.insert_one(post)
			info = QMessageBox()
			info.setWindowTitle("Apparatus registration")
			info.setText("Apparatus " +appname + " with id " + appid + " was registered successfully")
			#info.setText("Successful")
			info.exec_()
			self.hide()
			self.w = labfeed(username, uid)
			self.w.show()

	def consumenable(self):
		if self.ui.checkBox_Consume.isChecked():
			self.ui.lineEdit_Consume.setEnabled(True)
		else:
			self.ui.lineEdit_Consume.setEnabled(False)