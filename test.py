import sys
import pymongo
from PyQt5.QtWidgets import QDialog, QApplication,QMainWindow,QMessageBox
from PyQt5.QtGui import QPixmap
from mainwindow import *
from adminlogin import *
from specificfield import *
from adminpanel import *
from thermolabfeed import*
from adduser import*
from labfeed import*
from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://domelrmc:123@cluster0.chlnc11.mongodb.net/?retryWrites=true&w=majority")

class adduser(QDialog):
	
	def __init__(self):
		super().__init__()
		self.ui = Ui_adduser()
		self.ui.setupUi(self)
		
		self.ui.pushButton_exit.clicked.connect(self.close)
		self.ui.pushinit.clicked.connect(self.submit)
		
		self.show()
	
	#def uidchanger(self,uid):
		

	def submit(self):
		name = self.ui.lineEdit_name.text()
		uname = self.ui.lineEdit_uname.text()
		pasw = self.ui.lineEdit_pass.text()		

		info = QMessageBox()

		if pasw == self.ui.lineEdit_retypepass.text() :
			
			db = cluster["domepeople"]
			collection = db["appuser"]
			uidnum = collection.count_documents({}) + 1
			uid = uname + str(uidnum)
			self.ui.lineEdit_uid.setText(uid)

			post = {"_id": uid, "name": name, "uname":uname, "passw":pasw}
			
			collection.insert_one(post)
			info.setText("User Initiated with User ID : "+uid)
			info.setWindowTitle("Success")
			info.setIcon(QMessageBox.Information)
			info.exec_()

			self.hide()
			self.w = labfeed1(self.uname,self.uid)
			self.w.show();
		else:
			info.setText("Passwords do not match!")
			info.setWindowTitle("Error")
			info.setIcon(QMessageBox.Information)
			info.exec_()


class adminlogin (QDialog):
	def __init__(self):
		super().__init__()
		self.ui = Ui_adminlogin()
		self.ui.setupUi(self)
		self.ui.pushButton_back.clicked.connect(self.showmainwindow)
		self.ui.checkBox_showpass.stateChanged.connect(self.showpass)
		self.ui.pushButton_login.clicked.connect(self.checkadmin)
		self.show()

	def checkadmin(self):
		uname = self.ui.lineEdit_uname.text()
		passw = self.ui.lineEdit_pass.text()
		genpass=""
		
		db = cluster["domepeople"]
		collection = db["appuser"]
		correctpass = collection.find_one({"uname":uname})
		genpass = correctpass["passw"]
		uid = correctpass["_id"]
		if passw == genpass:
			self.hide()
			self.w = labfeed(uname,uid)
			self.w.show()
		elif uname == "admin" and passw == "newadminpass":
			self.hide()
			self.w = adminpanel("Admin")
			self.w.show()
		else:
			self.ui.label_warn.setText("Wrong username or Password!")

	def showpass(self):
		if self.ui.checkBox_showpass.isChecked():
			self.ui.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Normal)
		else:
			self.ui.lineEdit_pass.setEchoMode(QtWidgets.QLineEdit.Password)

	def showmainwindow(self):
		self.hide()
		self.w = mainwindow()
		self.w.show()

class thermolabfeed (QDialog):
	def __init__(self):
		super().__init__()
		self.ui = Ui_Thermolabfeed()
		self.ui.setupUi(self)
		self.show()
		self.ui.checkBox_Consume.stateChanged.connect(self.consumenable)
		self.ui.pushButton_submit.clicked.connect(self.submit)


	def submit(self):
		appid = self.ui.label_aid.text()
		appname = self.ui.lineEdit_Aname.text()
		condition = self.ui.comboBox_condition.currentText()
		demonstrations = self.ui.lineEdit_Demon.text()
		consumables = self.ui.lineEdit_Consume.text()
		description = self.ui.textEdit_description.toPlainText()

		
		db = cluster["domelabs"]
		collection = db["Thermolab"]
		appidnum = collection.count_documents({}) + 1
		appid = "TL" + str(appidnum)

		self.ui.label_aid.setText(appid)

		post = {"_id":appid,"name":appname, "condition":condition, "demos":demonstrations,"consume": consumables,"description":description}
		collection.insert_one(post)


	def consumenable(self):
		if self.ui.checkBox_Consume.isChecked():
			self.ui.lineEdit_Consume.setEnabled(True)
		else:
			self.ui.lineEdit_Consume.setEnabled(False)


class specificfield (QDialog):
	def __init__(self):
		super().__init__()
		self.ui = Ui_specificfield()
		self.ui.setupUi(self)
		self.show() 
		self.ui.pushButton_back.clicked.connect(self.showmainwindow)

	def showmainwindow(self):
		self.hide()
		self.w = mainwindow()
		self.w.show()

class mainwindow (QMainWindow):
	def __init__(self):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		pixmap = QPixmap('bg/logo.png')
		self.ui.pushButton_adminlogin.clicked.connect(self.showadmin)
		self.ui.pushButton_viewlabs.clicked.connect(self.showfield)
		self.ui.pushButton_close.clicked.connect(self.close)
		self.ui.pushButton_newaccount.clicked.connect(self.newuser)
		self.ui.label_logo.setPixmap(pixmap)
		self.ui.label_logo.setScaledContents(True)
		self.show()

	def newuser(self):
		self.hide()
		self.w = adduser()
		self.w.show()

	def showfield(self):
		self.hide()
		self.w = specificfield()
		self.w.show()

	def showadmin(self):
		self.hide()
		self.w = adminlogin()
		self.w.show()
	 	
class adminpanel (QDialog):
	def __init__(self,username):
		super().__init__()
		self.ui = Ui_adminpanel()
		self.ui.setupUi(self)
		self.user = username
		self.ui.pushButton.clicked.connect(self.showthermo)
		self.show()
		self.ui.pushButton_logout.clicked.connect(self.close)
		self.ui.pushButton_adduser_2.clicked.connect(self.showadduser)
		self.ui.label_welcome.setText("Hello "+ self.user)

	def showadduser(self):
		self.hide()
		self.w = adduser()
		self.w.show()

	def showthermo(self):
		self.hide()
		self.w = thermolabfeed()
		self.w.show()
	
class labfeed(QDialog):
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

if __name__=="__main__":
	app = QApplication(sys.argv)
	w = mainwindow()
	w.show()
	sys.exit(app.exec_())

