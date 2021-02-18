#!/bin/python3
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from pytube import YouTube
import pydub
import os
import random
import sys
class Window(QMainWindow):
	def __init__(self):
		super().__init__()
		self.setUI()
	def setUI(self):
		self.settings()
		self.mainMenu()
		self.show()
	def settings(self):
		self.setWindowTitle("YouTube Downloader")
		self.setGeometry(250,250,800,100)
		self.setMaximumSize(800,250)
		self.setMinimumSize(800,250)
	def mainMenu(self):
		widget = QWidget()
		hbox = QHBoxLayout()
		vbox = QVBoxLayout()
		label = QLabel("<b style=\"color:red\">Enter YouTube Link:</b>")
		self.label2 = QLabel(f"<b style=\"color:blue\">Location:</b> {os.getcwd()}")
		self.label3 = QLabel("")
		button2 = QPushButton("Change Directory")
		self.link = QLineEdit()
		self.link.setPlaceholderText("https://www.youtube.com/watch?v=rRPQs_kM_nw")
		self.mp4 = QRadioButton("MP4")
		self.mp3 = QRadioButton("MP3")
		self.button3 = QPushButton("Continue")
		button = QPushButton("Download")
		self.label4 = QLabel("")
		self.label4.setHidden(True)
		self.cbox = QComboBox()
		self.mp4.setChecked(True)
		hbox.addWidget(label)
		hbox.addWidget(self.link)
		self.button3.setHidden(True)
		hbox.addWidget(button)
		vbox.addWidget(self.mp4)
		vbox.addWidget(self.mp3)
		vbox.addWidget(self.label2)
		vbox.addWidget(button2)
		vbox.addLayout(hbox)
		vbox.addWidget(self.label4)
		vbox.addWidget(self.cbox)
		vbox.addWidget(self.button3)
		self.cbox.setHidden(True)
		vbox.addWidget(self.label3)
		widget.setLayout(vbox)
		self.setCentralWidget(widget)
		button.clicked.connect(self.download)
		self.mp3.toggled.connect(lambda:self.mp3time())
		self.link.textChanged.connect(self.clr)
		self.mp4.toggled.connect(lambda:self.mp4time())
		self.button3.clicked.connect(self.download_vid)
		button2.clicked.connect(self.chdir)
	def filterTitle(self,zTitle):
		zTitle = zTitle.replace("*","")
		zTitle = zTitle.replace("/","")
		zTitle = zTitle.replace("#","")
		zTitle = zTitle.replace("%","")
		zTitle = zTitle.replace("\"","")
		zTitle = zTitle.replace("'","")
		zTitle = zTitle.replace("^","")
		zTitle = zTitle.replace("?","")
		zTitle = zTitle.replace("'","")
		zTitle = zTitle.replace("$","")
		zTitle = zTitle.replace("\\","")
		zTitle = zTitle.replace("|","")
		zTitle = zTitle.replace(".","")
		zTitle = zTitle.replace(":","")
		zTitle = zTitle.replace(",","")
		zTitle = zTitle.replace(";","")
		zTitle = zTitle.replace("~","")
		return zTitle
	def clr(self):
		self.label3.setText("")
	def mp3time(self):
		self.cbox.setHidden(True)
		self.button3.setHidden(True)
		self.label3.setText("")
	def mp4time(self):
		if self.cbox.count()>0:
			self.cbox.setHidden(False)
			self.button3.setHidden(False)
		self.label3.setText("")
	def chdir(self):
		try:
			file = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
			os.chdir(file)
			self.label2.setText(f"<b style=\"color:blue\">Location:</b> {os.getcwd()}")
		except:
			pass
	def download(self):
		self.label3.setText("")
		try:
			self.cbox.clear()
			self.url = self.link.text()
			title = YouTube(self.url).title
			if YouTube(self.url).streams.filter(res="720p"):
				self.cbox.addItem("720p")
			if YouTube(self.url).streams.filter(res="360p"):
				self.cbox.addItem("360p")
				self.label4.setText(f"<b style=\"color:purple\">{title}</b>")
				self.label4.setHidden(False)
				if self.mp4.isChecked():
					self.label3.setText("")
					self.button3.setHidden(False)
					self.cbox.setHidden(False)
				else:
					self.button3.setHidden(True)
					self.cbox.setHidden(True)
					self.iTag=251
					stream = YouTube(self.url).streams.get_by_itag(self.iTag)
					stream.download()
					newName = self.filterTitle(title)
					self.changeExt(newName+".webm",newName)
					self.label4.setHidden(True)
					self.link.setText("")
					self.label3.setText("<b style=\"color:green\">Download Complete!</b>")
					self.cbox.clear()				
		except:
			self.link.setText("")
			self.label3.setText("<b style=\"color:red\">Please enter a valid YouTube link</b>")
	def download_vid(self):
		text = self.cbox.currentText()
		if text=="360p":
			YouTube(self.url).streams.get_by_itag(18).download()
		else:
			YouTube(self.url).streams.get_by_itag(22).download()
		self.link.setText("")
		self.label3.setText("<b style=\"color:green\">Download Complete!</b>")
		self.cbox.setHidden(True)
		self.button3.setHidden(True)
		self.label4.setHidden(True)
		self.cbox.clear()
	def changeExt(self,fileName,newName):		
		webm = pydub.AudioSegment.from_file(fileName, format="webm")
		webm.export(f"{newName}.mp3", format="mp3")
		os.remove(fileName)
if __name__ == "__main__":
	app = QApplication(sys.argv)
	windows = Window()
	sys.exit(app.exec())