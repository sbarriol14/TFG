# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vistaFES2.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

# LIBS
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep
from model.Devices import Devices
from pylsl import StreamInlet, resolve_stream


# Building*************************************************************************************************************
class LThread(QThread):
	# signaler = pyqtSignal(list)
	# boolean = False

	def run(self):
		# Resolve an available OpenSignals stream
		print("# Looking for an available OpenSignals stream...")
		os_stream = resolve_stream("name", "OpenSignals")
		print("Opensignals EMG signal detected")
		# Create an inlet to receive signal samples from the stream
		inlet = StreamInlet(os_stream[0])
		# Get information about the stream
		stream_info = inlet.info()
		# Get individual attributes
		stream_name = stream_info.name()
		stream_mac = stream_info.type()
		stream_host = stream_info.hostname()
		stream_n_channels = stream_info.channel_count()
		# Store sensor channel info & units in dictionary
		stream_channels = dict()
		channels = stream_info.desc().child("channels").child("channel")
		# Loop through all available channels
		for i in range(stream_n_channels - 1):
			# Get the channel number (e.g. 1)
			channel = i + 1
			# Get the channel type (e.g. EMG)
			sensor = channels.child_value("sensor")
			# Get the channel unit (e.g. mV)
			unit = channels.child_value("unit")
			# Store the information in the stream_channels dictionary
			stream_channels.update({channel: [sensor, unit]})
			channels = channels.next_sibling()
		print("Initiating EMG capt")
		# Loop for sampling
		while True:
			# Receive samples
			sample, timestamp = inlet.pull_sample()
			sample = list(sample)
			# sample list containing [time sec, voltage value]
			try:
				Ui_Form.devices.emgdev.add_sample(samplechunk=sample[1])
			except:
				print(Exception)
			# Resets signal if it gets too long for liberating memory
			Ui_Form.devices.emgdev.limit_chunk()
			# Threshold method to detect muscular contractions
			if Ui_Form.devices.emgdev.calibration_threshold != 0:
				lastnum = Ui_Form
				if lastnum > Ui_Form.devices.emgdev.calibration_threshold:
					Ui_Form.devices.emgdev.activate_boolean()


# Building*************************************************************************************************************
class SThread(QThread):

	def run(self):
		print("Stimulator ready")
		while True:
			if Ui_Form.devices.emgdev.actfes:
				maska = Ui_Form.devices.fesdev.mask
				Ui_Form.devices.fesdev.stimulation(maska)
				Ui_Form.devices.emgdev.deactivate_boolean()

# Interface class
class Ui_Form(object):
	devices = Devices()
	numberCOM = 0

	def setupUi(self, Form):


		Form.setObjectName("Form")
		Form.resize(722, 484)
		self.exitbutt2 = QtWidgets.QPushButton(Form)
		self.exitbutt2.setGeometry(QtCore.QRect(610, 430, 101, 51))
		font = QtGui.QFont()
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.exitbutt2.setFont(font)
		self.exitbutt2.setObjectName("exitbutt2")
		self.conectarcombutt = QtWidgets.QPushButton(Form)
		self.conectarcombutt.setGeometry(QtCore.QRect(10, 20, 101, 41))
		self.conectarcombutt.setObjectName("conectarcombutt")
		self.line_2 = QtWidgets.QFrame(Form)
		self.line_2.setGeometry(QtCore.QRect(0, 150, 251, 16))
		self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
		self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_2.setObjectName("line_2")
		self.line_3 = QtWidgets.QFrame(Form)
		self.line_3.setGeometry(QtCore.QRect(240, 0, 20, 161))
		self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
		self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
		self.line_3.setObjectName("line_3")
		self.infochannels = QtWidgets.QGroupBox(Form)
		self.infochannels.setGeometry(QtCore.QRect(340, 10, 451, 321))
		self.infochannels.setObjectName("infochannels")
		self.channtablab = QtWidgets.QLabel(self.infochannels)
		self.channtablab.setGeometry(QtCore.QRect(30, 30, 51, 20))
		font = QtGui.QFont()
		font.setUnderline(True)
		self.channtablab.setFont(font)
		self.channtablab.setObjectName("channtablab")
		self.channtablab_3 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_3.setGeometry(QtCore.QRect(110, 30, 71, 20))
		font = QtGui.QFont()
		font.setUnderline(True)
		self.channtablab_3.setFont(font)
		self.channtablab_3.setObjectName("channtablab_3")
		self.channtablab_4 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_4.setGeometry(QtCore.QRect(190, 30, 51, 20))
		font = QtGui.QFont()
		font.setUnderline(True)
		self.channtablab_4.setFont(font)
		self.channtablab_4.setObjectName("channtablab_4")
		self.channtablab_5 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_5.setGeometry(QtCore.QRect(300, 30, 41, 20))
		font = QtGui.QFont()
		font.setUnderline(True)
		self.channtablab_5.setFont(font)
		self.channtablab_5.setObjectName("channtablab_5")
		self.channtablab_6 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_6.setGeometry(QtCore.QRect(250, 30, 41, 20))
		font = QtGui.QFont()
		font.setUnderline(True)
		self.channtablab_6.setFont(font)
		self.channtablab_6.setObjectName("channtablab_6")
		self.channtablab_7 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_7.setGeometry(QtCore.QRect(350, 30, 21, 16))
		font = QtGui.QFont()
		font.setUnderline(True)
		self.channtablab_7.setFont(font)
		self.channtablab_7.setObjectName("channtablab_7")
		self.channtablab_2 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_2.setGeometry(QtCore.QRect(30, 60, 51, 20))
		font = QtGui.QFont()
		font.setUnderline(False)
		self.channtablab_2.setFont(font)
		self.channtablab_2.setObjectName("channtablab_2")
		self.channtablab_8 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_8.setGeometry(QtCore.QRect(30, 90, 51, 20))
		font = QtGui.QFont()
		font.setUnderline(False)
		self.channtablab_8.setFont(font)
		self.channtablab_8.setObjectName("channtablab_8")
		self.channtablab_9 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_9.setGeometry(QtCore.QRect(30, 120, 51, 20))
		font = QtGui.QFont()
		font.setUnderline(False)
		self.channtablab_9.setFont(font)
		self.channtablab_9.setObjectName("channtablab_9")
		self.channtablab_10 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_10.setGeometry(QtCore.QRect(30, 150, 51, 20))
		font = QtGui.QFont()
		font.setUnderline(False)
		self.channtablab_10.setFont(font)
		self.channtablab_10.setObjectName("channtablab_10")
		self.channtablab_11 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_11.setGeometry(QtCore.QRect(30, 180, 51, 20))
		font = QtGui.QFont()
		font.setUnderline(False)
		self.channtablab_11.setFont(font)
		self.channtablab_11.setObjectName("channtablab_11")
		self.channtablab_12 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_12.setGeometry(QtCore.QRect(30, 210, 51, 20))
		font = QtGui.QFont()
		font.setUnderline(False)
		self.channtablab_12.setFont(font)
		self.channtablab_12.setObjectName("channtablab_12")
		self.channtablab_13 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_13.setGeometry(QtCore.QRect(30, 240, 51, 20))
		font = QtGui.QFont()
		font.setUnderline(False)
		self.channtablab_13.setFont(font)
		self.channtablab_13.setObjectName("channtablab_13")
		self.channtablab_14 = QtWidgets.QLabel(self.infochannels)
		self.channtablab_14.setGeometry(QtCore.QRect(30, 270, 51, 20))
		font = QtGui.QFont()
		font.setUnderline(False)
		self.channtablab_14.setFont(font)
		self.channtablab_14.setObjectName("channtablab_14")
		self.currentnum_1 = QtWidgets.QLabel(self.infochannels)
		self.currentnum_1.setGeometry(QtCore.QRect(120, 60, 31, 16))
		self.currentnum_1.setMouseTracking(True)
		self.currentnum_1.setAlignment(QtCore.Qt.AlignCenter)
		self.currentnum_1.setObjectName("currentnum_1")
		self.currentnum_2 = QtWidgets.QLabel(self.infochannels)
		self.currentnum_2.setGeometry(QtCore.QRect(120, 90, 31, 16))
		self.currentnum_2.setMouseTracking(True)
		self.currentnum_2.setAlignment(QtCore.Qt.AlignCenter)
		self.currentnum_2.setObjectName("currentnum_2")
		self.currentnum_3 = QtWidgets.QLabel(self.infochannels)
		self.currentnum_3.setGeometry(QtCore.QRect(120, 120, 31, 16))
		self.currentnum_3.setMouseTracking(True)
		self.currentnum_3.setAlignment(QtCore.Qt.AlignCenter)
		self.currentnum_3.setObjectName("currentnum_3")
		self.currentnum_4 = QtWidgets.QLabel(self.infochannels)
		self.currentnum_4.setGeometry(QtCore.QRect(120, 150, 31, 16))
		self.currentnum_4.setMouseTracking(True)
		self.currentnum_4.setAlignment(QtCore.Qt.AlignCenter)
		self.currentnum_4.setObjectName("currentnum_4")
		self.currentnum_5 = QtWidgets.QLabel(self.infochannels)
		self.currentnum_5.setGeometry(QtCore.QRect(120, 180, 31, 16))
		self.currentnum_5.setMouseTracking(True)
		self.currentnum_5.setAlignment(QtCore.Qt.AlignCenter)
		self.currentnum_5.setObjectName("currentnum_5")
		self.currentnum_6 = QtWidgets.QLabel(self.infochannels)
		self.currentnum_6.setGeometry(QtCore.QRect(120, 210, 31, 16))
		self.currentnum_6.setMouseTracking(True)
		self.currentnum_6.setAlignment(QtCore.Qt.AlignCenter)
		self.currentnum_6.setObjectName("currentnum_6")
		self.currentnum_7 = QtWidgets.QLabel(self.infochannels)
		self.currentnum_7.setGeometry(QtCore.QRect(120, 240, 31, 16))
		self.currentnum_7.setMouseTracking(True)
		self.currentnum_7.setAlignment(QtCore.Qt.AlignCenter)
		self.currentnum_7.setObjectName("currentnum_7")
		self.currentnum_8 = QtWidgets.QLabel(self.infochannels)
		self.currentnum_8.setGeometry(QtCore.QRect(120, 270, 31, 16))
		self.currentnum_8.setMouseTracking(True)
		self.currentnum_8.setAlignment(QtCore.Qt.AlignCenter)
		self.currentnum_8.setObjectName("currentnum_8")
		self.freqnum_1 = QtWidgets.QLabel(self.infochannels)
		self.freqnum_1.setGeometry(QtCore.QRect(190, 60, 31, 16))
		self.freqnum_1.setMouseTracking(True)
		self.freqnum_1.setAlignment(QtCore.Qt.AlignCenter)
		self.freqnum_1.setObjectName("freqnum_1")
		self.freqnum_2 = QtWidgets.QLabel(self.infochannels)
		self.freqnum_2.setGeometry(QtCore.QRect(190, 90, 31, 16))
		self.freqnum_2.setMouseTracking(True)
		self.freqnum_2.setAlignment(QtCore.Qt.AlignCenter)
		self.freqnum_2.setObjectName("freqnum_2")
		self.freqnum_3 = QtWidgets.QLabel(self.infochannels)
		self.freqnum_3.setGeometry(QtCore.QRect(190, 120, 31, 16))
		self.freqnum_3.setMouseTracking(True)
		self.freqnum_3.setAlignment(QtCore.Qt.AlignCenter)
		self.freqnum_3.setObjectName("freqnum_3")
		self.freqnum_4 = QtWidgets.QLabel(self.infochannels)
		self.freqnum_4.setGeometry(QtCore.QRect(190, 150, 31, 16))
		self.freqnum_4.setMouseTracking(True)
		self.freqnum_4.setAlignment(QtCore.Qt.AlignCenter)
		self.freqnum_4.setObjectName("freqnum_4")
		self.freqnum_5 = QtWidgets.QLabel(self.infochannels)
		self.freqnum_5.setGeometry(QtCore.QRect(190, 180, 31, 16))
		self.freqnum_5.setMouseTracking(True)
		self.freqnum_5.setAlignment(QtCore.Qt.AlignCenter)
		self.freqnum_5.setObjectName("freqnum_5")
		self.freqnum_6 = QtWidgets.QLabel(self.infochannels)
		self.freqnum_6.setGeometry(QtCore.QRect(190, 210, 31, 16))
		self.freqnum_6.setMouseTracking(True)
		self.freqnum_6.setAlignment(QtCore.Qt.AlignCenter)
		self.freqnum_6.setObjectName("freqnum_6")
		self.freqnum_7 = QtWidgets.QLabel(self.infochannels)
		self.freqnum_7.setGeometry(QtCore.QRect(190, 240, 31, 16))
		self.freqnum_7.setMouseTracking(True)
		self.freqnum_7.setAlignment(QtCore.Qt.AlignCenter)
		self.freqnum_7.setObjectName("freqnum_7")
		self.freqnum_8 = QtWidgets.QLabel(self.infochannels)
		self.freqnum_8.setGeometry(QtCore.QRect(190, 270, 31, 16))
		self.freqnum_8.setMouseTracking(True)
		self.freqnum_8.setAlignment(QtCore.Qt.AlignCenter)
		self.freqnum_8.setObjectName("freqnum_8")
		self.pwnum_1 = QtWidgets.QLabel(self.infochannels)
		self.pwnum_1.setGeometry(QtCore.QRect(250, 60, 31, 16))
		self.pwnum_1.setMouseTracking(True)
		self.pwnum_1.setAlignment(QtCore.Qt.AlignCenter)
		self.pwnum_1.setObjectName("pwnum_1")
		self.pwnum_2 = QtWidgets.QLabel(self.infochannels)
		self.pwnum_2.setGeometry(QtCore.QRect(250, 90, 31, 16))
		self.pwnum_2.setMouseTracking(True)
		self.pwnum_2.setAlignment(QtCore.Qt.AlignCenter)
		self.pwnum_2.setObjectName("pwnum_2")
		self.pwnum_3 = QtWidgets.QLabel(self.infochannels)
		self.pwnum_3.setGeometry(QtCore.QRect(250, 120, 31, 16))
		self.pwnum_3.setMouseTracking(True)
		self.pwnum_3.setAlignment(QtCore.Qt.AlignCenter)
		self.pwnum_3.setObjectName("pwnum_3")
		self.pwnum_4 = QtWidgets.QLabel(self.infochannels)
		self.pwnum_4.setGeometry(QtCore.QRect(250, 150, 31, 16))
		self.pwnum_4.setMouseTracking(True)
		self.pwnum_4.setAlignment(QtCore.Qt.AlignCenter)
		self.pwnum_4.setObjectName("pwnum_4")
		self.pwnum_5 = QtWidgets.QLabel(self.infochannels)
		self.pwnum_5.setGeometry(QtCore.QRect(250, 180, 31, 16))
		self.pwnum_5.setMouseTracking(True)
		self.pwnum_5.setAlignment(QtCore.Qt.AlignCenter)
		self.pwnum_5.setObjectName("pwnum_5")
		self.pwnum_6 = QtWidgets.QLabel(self.infochannels)
		self.pwnum_6.setGeometry(QtCore.QRect(250, 210, 31, 16))
		self.pwnum_6.setMouseTracking(True)
		self.pwnum_6.setAlignment(QtCore.Qt.AlignCenter)
		self.pwnum_6.setObjectName("pwnum_6")
		self.pwnum_7 = QtWidgets.QLabel(self.infochannels)
		self.pwnum_7.setGeometry(QtCore.QRect(250, 240, 31, 16))
		self.pwnum_7.setMouseTracking(True)
		self.pwnum_7.setAlignment(QtCore.Qt.AlignCenter)
		self.pwnum_7.setObjectName("pwnum_7")
		self.pwnum_8 = QtWidgets.QLabel(self.infochannels)
		self.pwnum_8.setGeometry(QtCore.QRect(250, 270, 31, 16))
		self.pwnum_8.setMouseTracking(True)
		self.pwnum_8.setAlignment(QtCore.Qt.AlignCenter)
		self.pwnum_8.setObjectName("pwnum_8")
		self.pnnum_1 = QtWidgets.QLabel(self.infochannels)
		self.pnnum_1.setGeometry(QtCore.QRect(340, 60, 31, 16))
		self.pnnum_1.setMouseTracking(True)
		self.pnnum_1.setAlignment(QtCore.Qt.AlignCenter)
		self.pnnum_1.setObjectName("pnnum_1")
		self.pnnum_2 = QtWidgets.QLabel(self.infochannels)
		self.pnnum_2.setGeometry(QtCore.QRect(340, 90, 31, 16))
		self.pnnum_2.setMouseTracking(True)
		self.pnnum_2.setAlignment(QtCore.Qt.AlignCenter)
		self.pnnum_2.setObjectName("pnnum_2")
		self.pnnum_3 = QtWidgets.QLabel(self.infochannels)
		self.pnnum_3.setGeometry(QtCore.QRect(340, 120, 31, 16))
		self.pnnum_3.setMouseTracking(True)
		self.pnnum_3.setAlignment(QtCore.Qt.AlignCenter)
		self.pnnum_3.setObjectName("pnnum_3")
		self.pnnum_4 = QtWidgets.QLabel(self.infochannels)
		self.pnnum_4.setGeometry(QtCore.QRect(340, 150, 31, 16))
		self.pnnum_4.setMouseTracking(True)
		self.pnnum_4.setAlignment(QtCore.Qt.AlignCenter)
		self.pnnum_4.setObjectName("pnnum_4")
		self.pnnum_5 = QtWidgets.QLabel(self.infochannels)
		self.pnnum_5.setGeometry(QtCore.QRect(340, 180, 31, 16))
		self.pnnum_5.setMouseTracking(True)
		self.pnnum_5.setAlignment(QtCore.Qt.AlignCenter)
		self.pnnum_5.setObjectName("pnnum_5")
		self.pnnum_6 = QtWidgets.QLabel(self.infochannels)
		self.pnnum_6.setGeometry(QtCore.QRect(340, 210, 31, 16))
		self.pnnum_6.setMouseTracking(True)
		self.pnnum_6.setAlignment(QtCore.Qt.AlignCenter)
		self.pnnum_6.setObjectName("pnnum_6")
		self.pnnum_7 = QtWidgets.QLabel(self.infochannels)
		self.pnnum_7.setGeometry(QtCore.QRect(340, 240, 31, 16))
		self.pnnum_7.setMouseTracking(True)
		self.pnnum_7.setAlignment(QtCore.Qt.AlignCenter)
		self.pnnum_7.setObjectName("pnnum_7")
		self.pnnum_8 = QtWidgets.QLabel(self.infochannels)
		self.pnnum_8.setGeometry(QtCore.QRect(340, 270, 31, 16))
		self.pnnum_8.setMouseTracking(True)
		self.pnnum_8.setAlignment(QtCore.Qt.AlignCenter)
		self.pnnum_8.setObjectName("pnnum_8")
		self.dtnum_1 = QtWidgets.QLabel(self.infochannels)
		self.dtnum_1.setGeometry(QtCore.QRect(300, 60, 31, 16))
		self.dtnum_1.setMouseTracking(True)
		self.dtnum_1.setAlignment(QtCore.Qt.AlignCenter)
		self.dtnum_1.setObjectName("dtnum_1")
		self.dtnum_2 = QtWidgets.QLabel(self.infochannels)
		self.dtnum_2.setGeometry(QtCore.QRect(300, 90, 31, 16))
		self.dtnum_2.setMouseTracking(True)
		self.dtnum_2.setAlignment(QtCore.Qt.AlignCenter)
		self.dtnum_2.setObjectName("dtnum_2")
		self.dtnum_3 = QtWidgets.QLabel(self.infochannels)
		self.dtnum_3.setGeometry(QtCore.QRect(300, 120, 31, 16))
		self.dtnum_3.setMouseTracking(True)
		self.dtnum_3.setAlignment(QtCore.Qt.AlignCenter)
		self.dtnum_3.setObjectName("dtnum_3")
		self.dtnum_4 = QtWidgets.QLabel(self.infochannels)
		self.dtnum_4.setGeometry(QtCore.QRect(300, 150, 31, 16))
		self.dtnum_4.setMouseTracking(True)
		self.dtnum_4.setAlignment(QtCore.Qt.AlignCenter)
		self.dtnum_4.setObjectName("dtnum_4")
		self.dtnum_5 = QtWidgets.QLabel(self.infochannels)
		self.dtnum_5.setGeometry(QtCore.QRect(300, 180, 31, 16))
		self.dtnum_5.setMouseTracking(True)
		self.dtnum_5.setAlignment(QtCore.Qt.AlignCenter)
		self.dtnum_5.setObjectName("dtnum_5")
		self.dtnum_6 = QtWidgets.QLabel(self.infochannels)
		self.dtnum_6.setGeometry(QtCore.QRect(300, 210, 31, 16))
		self.dtnum_6.setMouseTracking(True)
		self.dtnum_6.setAlignment(QtCore.Qt.AlignCenter)
		self.dtnum_6.setObjectName("dtnum_6")
		self.dtnum_7 = QtWidgets.QLabel(self.infochannels)
		self.dtnum_7.setGeometry(QtCore.QRect(300, 240, 31, 16))
		self.dtnum_7.setMouseTracking(True)
		self.dtnum_7.setAlignment(QtCore.Qt.AlignCenter)
		self.dtnum_7.setObjectName("dtnum_7")
		self.dtnum_8 = QtWidgets.QLabel(self.infochannels)
		self.dtnum_8.setGeometry(QtCore.QRect(300, 270, 31, 16))
		self.dtnum_8.setMouseTracking(True)
		self.dtnum_8.setAlignment(QtCore.Qt.AlignCenter)
		self.dtnum_8.setObjectName("dtnum_8")
		self.fesoffbutt = QtWidgets.QPushButton(Form)
		self.fesoffbutt.setGeometry(QtCore.QRect(120, 100, 91, 41))
		self.fesoffbutt.setObjectName("fesoffbutt")
		self.deconectccombutt = QtWidgets.QPushButton(Form)
		self.deconectccombutt.setGeometry(QtCore.QRect(120, 20, 101, 51))
		self.deconectccombutt.setObjectName("deconectccombutt")
		self.paramframe = QtWidgets.QGroupBox(Form)
		self.paramframe.setGeometry(QtCore.QRect(0, 170, 331, 281))
		self.paramframe.setObjectName("paramframe")
		self.maskbutt = QtWidgets.QPushButton(self.paramframe)
		self.maskbutt.setGeometry(QtCore.QRect(230, 20, 91, 31))
		font = QtGui.QFont()
		font.setItalic(True)
		self.maskbutt.setFont(font)
		self.maskbutt.setObjectName("maskbutt")
		self.currentbutt = QtWidgets.QPushButton(self.paramframe)
		self.currentbutt.setGeometry(QtCore.QRect(10, 60, 91, 31))
		self.currentbutt.setObjectName("currentbutt")
		self.freqbutt = QtWidgets.QPushButton(self.paramframe)
		self.freqbutt.setGeometry(QtCore.QRect(120, 60, 91, 31))
		self.freqbutt.setObjectName("freqbutt")
		self.pwbutt = QtWidgets.QPushButton(self.paramframe)
		self.pwbutt.setGeometry(QtCore.QRect(10, 130, 91, 31))
		self.pwbutt.setObjectName("pwbutt")
		self.dtbutt = QtWidgets.QPushButton(self.paramframe)
		self.dtbutt.setGeometry(QtCore.QRect(120, 130, 91, 31))
		self.dtbutt.setObjectName("dtbutt")
		self.pnbutt = QtWidgets.QPushButton(self.paramframe)
		self.pnbutt.setGeometry(QtCore.QRect(10, 200, 91, 31))
		self.pnbutt.setObjectName("pnbutt")
		self.currentnum = QtWidgets.QLineEdit(self.paramframe)
		self.currentnum.setGeometry(QtCore.QRect(10, 100, 91, 21))
		self.currentnum.setAlignment(QtCore.Qt.AlignCenter)
		self.currentnum.setObjectName("currentnum")
		self.freqnum = QtWidgets.QLineEdit(self.paramframe)
		self.freqnum.setGeometry(QtCore.QRect(120, 100, 91, 21))
		self.freqnum.setAlignment(QtCore.Qt.AlignCenter)
		self.freqnum.setObjectName("freqnum")
		self.pwnum = QtWidgets.QLineEdit(self.paramframe)
		self.pwnum.setGeometry(QtCore.QRect(10, 170, 91, 21))
		self.pwnum.setAlignment(QtCore.Qt.AlignCenter)
		self.pwnum.setObjectName("pwnum")
		self.dtnum = QtWidgets.QLineEdit(self.paramframe)
		self.dtnum.setGeometry(QtCore.QRect(120, 170, 91, 21))
		self.dtnum.setAlignment(QtCore.Qt.AlignCenter)
		self.dtnum.setObjectName("dtnum")
		self.pnnum = QtWidgets.QLineEdit(self.paramframe)
		self.pnnum.setGeometry(QtCore.QRect(10, 240, 91, 16))
		self.pnnum.setAlignment(QtCore.Qt.AlignCenter)
		self.pnnum.setObjectName("pnnum")
		self.sendparambutt = QtWidgets.QPushButton(self.paramframe)
		self.sendparambutt.setGeometry(QtCore.QRect(110, 200, 101, 61))
		self.sendparambutt.setObjectName("sendparambutt")
		self.channelselecframe_2 = QtWidgets.QGroupBox(self.paramframe)
		self.channelselecframe_2.setGeometry(QtCore.QRect(230, 60, 91, 201))
		self.channelselecframe_2.setObjectName("channelselecframe_2")
		self.fcheckch1 = QtWidgets.QCheckBox(self.channelselecframe_2)
		self.fcheckch1.setGeometry(QtCore.QRect(20, 30, 70, 17))
		self.fcheckch1.setMouseTracking(False)
		self.fcheckch1.setChecked(False)
		self.fcheckch1.setObjectName("fcheckch1")
		self.fcheckch2 = QtWidgets.QCheckBox(self.channelselecframe_2)
		self.fcheckch2.setGeometry(QtCore.QRect(20, 50, 61, 17))
		self.fcheckch2.setChecked(True)
		self.fcheckch2.setObjectName("fcheckch2")
		self.fcheckch3 = QtWidgets.QCheckBox(self.channelselecframe_2)
		self.fcheckch3.setGeometry(QtCore.QRect(20, 70, 70, 17))
		self.fcheckch3.setChecked(False)
		self.fcheckch3.setObjectName("fcheckch3")
		self.fcheckch4 = QtWidgets.QCheckBox(self.channelselecframe_2)
		self.fcheckch4.setGeometry(QtCore.QRect(20, 90, 70, 17))
		self.fcheckch4.setObjectName("fcheckch4")
		self.fcheckch5 = QtWidgets.QCheckBox(self.channelselecframe_2)
		self.fcheckch5.setGeometry(QtCore.QRect(20, 110, 70, 17))
		self.fcheckch5.setMouseTracking(False)
		self.fcheckch5.setChecked(False)
		self.fcheckch5.setObjectName("fcheckch5")
		self.fcheckch6 = QtWidgets.QCheckBox(self.channelselecframe_2)
		self.fcheckch6.setGeometry(QtCore.QRect(20, 130, 70, 17))
		self.fcheckch6.setMouseTracking(False)
		self.fcheckch6.setChecked(False)
		self.fcheckch6.setObjectName("fcheckch6")
		self.fcheckch7 = QtWidgets.QCheckBox(self.channelselecframe_2)
		self.fcheckch7.setGeometry(QtCore.QRect(20, 150, 70, 17))
		self.fcheckch7.setMouseTracking(False)
		self.fcheckch7.setChecked(False)
		self.fcheckch7.setObjectName("fcheckch7")
		self.fcheckch8 = QtWidgets.QCheckBox(self.channelselecframe_2)
		self.fcheckch8.setGeometry(QtCore.QRect(20, 170, 70, 17))
		self.fcheckch8.setMouseTracking(False)
		self.fcheckch8.setChecked(False)
		self.fcheckch8.setObjectName("fcheckch8")
		self.fesonbutt = QtWidgets.QPushButton(Form)
		self.fesonbutt.setGeometry(QtCore.QRect(10, 100, 91, 41))
		self.fesonbutt.setObjectName("fesonbutt")
		self.numerocomdisp = QtWidgets.QLineEdit(Form)
		self.numerocomdisp.setGeometry(QtCore.QRect(61, 60, 20, 20))
		self.numerocomdisp.setAlignment(QtCore.Qt.AlignCenter)
		self.numerocomdisp.setObjectName("numerocomdisp")
		self.toolButton = QtWidgets.QToolButton(Form)
		self.toolButton.setEnabled(True)
		self.toolButton.setGeometry(QtCore.QRect(34, 60, 31, 20))
		self.toolButton.setObjectName("toolButton")
		self.EMG = QtWidgets.QFrame(Form)
		self.EMG.setGeometry(QtCore.QRect(340, 330, 391, 121))
		self.EMG.setFrameShape(QtWidgets.QFrame.StyledPanel)
		self.EMG.setFrameShadow(QtWidgets.QFrame.Raised)
		self.EMG.setObjectName("EMG")
		self.calibbutt = QtWidgets.QPushButton(self.EMG)
		self.calibbutt.setGeometry(QtCore.QRect(20, 70, 211, 41))
		font = QtGui.QFont()
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.calibbutt.setFont(font)
		self.calibbutt.setObjectName("calibbutt")
		self.emgstopbutt = QtWidgets.QPushButton(self.EMG)
		self.emgstopbutt.setGeometry(QtCore.QRect(230, 10, 141, 41))
		font = QtGui.QFont()
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.emgstopbutt.setFont(font)
		self.emgstopbutt.setObjectName("emgstopbutt")
		self.emglistenerbutt = QtWidgets.QPushButton(self.EMG)
		self.emglistenerbutt.setGeometry(QtCore.QRect(20, 10, 181, 41))
		font = QtGui.QFont()
		font.setPointSize(14)
		font.setBold(True)
		font.setWeight(75)
		self.emglistenerbutt.setFont(font)
		self.emglistenerbutt.setObjectName("emglistenerbutt")
		self.EMG.raise_()
		self.exitbutt2.raise_()
		self.conectarcombutt.raise_()
		self.line_2.raise_()
		self.line_3.raise_()
		self.infochannels.raise_()
		self.fesoffbutt.raise_()
		self.deconectccombutt.raise_()
		self.paramframe.raise_()
		self.fesonbutt.raise_()
		self.numerocomdisp.raise_()
		self.toolButton.raise_()
		self.connectAll()

		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "Form"))
		self.exitbutt2.setText(_translate("Form", "Salir"))
		self.conectarcombutt.setText(_translate("Form", "Conectar COM"))
		self.infochannels.setTitle(_translate("Form", "Canales (Tabla lectura parametros)"))
		self.channtablab.setText(_translate("Form", "Canales"))
		self.channtablab_3.setText(_translate("Form", "Current (mA)"))
		self.channtablab_4.setText(_translate("Form", "Freq (Hz)"))
		self.channtablab_5.setText(_translate("Form", "DT (ms)"))
		self.channtablab_6.setText(_translate("Form", "PW (us)"))
		self.channtablab_7.setText(_translate("Form", "PN"))
		self.channtablab_2.setText(_translate("Form", "Canal 1"))
		self.channtablab_8.setText(_translate("Form", "Canal 2"))
		self.channtablab_9.setText(_translate("Form", "Canal 3"))
		self.channtablab_10.setText(_translate("Form", "Canal 4"))
		self.channtablab_11.setText(_translate("Form", "Canal 5"))
		self.channtablab_12.setText(_translate("Form", "Canal 6"))
		self.channtablab_13.setText(_translate("Form", "Canal 7"))
		self.channtablab_14.setText(_translate("Form", "Canal 8"))
		self.currentnum_1.setText(_translate("Form", "0"))
		self.currentnum_2.setText(_translate("Form", "0"))
		self.currentnum_3.setText(_translate("Form", "0"))
		self.currentnum_4.setText(_translate("Form", "0"))
		self.currentnum_5.setText(_translate("Form", "0"))
		self.currentnum_6.setText(_translate("Form", "0"))
		self.currentnum_7.setText(_translate("Form", "0"))
		self.currentnum_8.setText(_translate("Form", "0"))
		self.freqnum_1.setText(_translate("Form", "0"))
		self.freqnum_2.setText(_translate("Form", "0"))
		self.freqnum_3.setText(_translate("Form", "0"))
		self.freqnum_4.setText(_translate("Form", "0"))
		self.freqnum_5.setText(_translate("Form", "0"))
		self.freqnum_6.setText(_translate("Form", "0"))
		self.freqnum_7.setText(_translate("Form", "0"))
		self.freqnum_8.setText(_translate("Form", "0"))
		self.pwnum_1.setText(_translate("Form", "0"))
		self.pwnum_2.setText(_translate("Form", "0"))
		self.pwnum_3.setText(_translate("Form", "0"))
		self.pwnum_4.setText(_translate("Form", "0"))
		self.pwnum_5.setText(_translate("Form", "0"))
		self.pwnum_6.setText(_translate("Form", "0"))
		self.pwnum_7.setText(_translate("Form", "0"))
		self.pwnum_8.setText(_translate("Form", "0"))
		self.pnnum_1.setText(_translate("Form", "0"))
		self.pnnum_2.setText(_translate("Form", "0"))
		self.pnnum_3.setText(_translate("Form", "0"))
		self.pnnum_4.setText(_translate("Form", "0"))
		self.pnnum_5.setText(_translate("Form", "0"))
		self.pnnum_6.setText(_translate("Form", "0"))
		self.pnnum_7.setText(_translate("Form", "0"))
		self.pnnum_8.setText(_translate("Form", "0"))
		self.dtnum_1.setText(_translate("Form", "0"))
		self.dtnum_2.setText(_translate("Form", "0"))
		self.dtnum_3.setText(_translate("Form", "0"))
		self.dtnum_4.setText(_translate("Form", "0"))
		self.dtnum_5.setText(_translate("Form", "0"))
		self.dtnum_6.setText(_translate("Form", "0"))
		self.dtnum_7.setText(_translate("Form", "0"))
		self.dtnum_8.setText(_translate("Form", "0"))
		self.fesoffbutt.setText(_translate("Form", "FES OFF"))
		self.deconectccombutt.setText(_translate("Form", "Desconectar COM"))
		self.paramframe.setTitle(_translate("Form", "Parámetros de canal"))
		self.maskbutt.setText(_translate("Form", "Set Mask"))
		self.currentbutt.setText(_translate("Form", "Set Current (mA)"))
		self.freqbutt.setText(_translate("Form", "Set Freq (Hz)"))
		self.pwbutt.setText(_translate("Form", "Set PW"))
		self.dtbutt.setText(_translate("Form", "Set DT"))
		self.pnbutt.setText(_translate("Form", "Set PN"))
		self.currentnum.setText(_translate("Form", "5"))
		self.freqnum.setText(_translate("Form", "30"))
		self.pwnum.setText(_translate("Form", "350"))
		self.dtnum.setText(_translate("Form", "0"))
		self.pnnum.setText(_translate("Form", "0"))
		self.sendparambutt.setText(_translate("Form", "Enviar parametros"))
		self.channelselecframe_2.setTitle(_translate("Form", "Selección Canal"))
		self.fcheckch1.setText(_translate("Form", "CH1"))
		self.fcheckch2.setText(_translate("Form", "CH2"))
		self.fcheckch3.setText(_translate("Form", "CH3"))
		self.fcheckch4.setText(_translate("Form", "CH4"))
		self.fcheckch5.setText(_translate("Form", "CH5"))
		self.fcheckch6.setText(_translate("Form", "CH6"))
		self.fcheckch7.setText(_translate("Form", "CH7"))
		self.fcheckch8.setText(_translate("Form", "CH8"))
		self.fesonbutt.setText(_translate("Form", "FES ON"))
		self.numerocomdisp.setText(_translate("Form", "0"))
		self.toolButton.setText(_translate("Form", "COM"))
		self.calibbutt.setText(_translate("Form", "Calibrate threshold"))
		self.emgstopbutt.setText(_translate("Form", "Stop EMG "))
		self.emglistenerbutt.setText(_translate("Form", "Start EMG "))





	# Conecct buttons of UI
	def connectAll(self):
		# FES
		self.numerocomdisp.textChanged.connect(self.onTextChangedComNum)
		self.conectarcombutt.clicked.connect(self.onClickConectarComButt)
		self.deconectccombutt.clicked.connect(self.onClickDeConectarComButt)
		self.fesonbutt.clicked.connect(self.onClickfesOnButt)
		self.fesoffbutt.clicked.connect(self.onClickfesOffButt)
		self.currentbutt.clicked.connect(self.onClickCurrentButt)
		self.freqbutt.clicked.connect(self.onClickFreqButt)
		self.pnbutt.clicked.connect(self.onClickPNButt)
		self.pwbutt.clicked.connect(self.onClickPWButt)
		self.dtbutt.clicked.connect(self.onClickDTButt)
		self.currentnum.textChanged.connect(self.onTextChangedCurrentNum)
		self.freqnum.textChanged.connect(self.onTextChangedFreqNum)
		self.pwnum.textChanged.connect(self.onTextChangedPWNum)
		self.dtnum.textChanged.connect(self.onTextChangedDTNum)
		self.pnnum.textChanged.connect(self.onTextChangedPNNum)
		self.fcheckch1.stateChanged.connect(self.onStateChangedFcheckch1)
		self.fcheckch2.stateChanged.connect(self.onStateChangedFcheckch2)
		self.fcheckch3.stateChanged.connect(self.onStateChangedFcheckch3)
		self.fcheckch4.stateChanged.connect(self.onStateChangedFcheckch4)
		self.fcheckch5.stateChanged.connect(self.onStateChangedFcheckch5)
		self.fcheckch6.stateChanged.connect(self.onStateChangedFcheckch6)
		self.fcheckch7.stateChanged.connect(self.onStateChangedFcheckch7)
		self.fcheckch8.stateChanged.connect(self.onStateChangedFcheckch8)
		self.maskbutt.clicked.connect(self.onClickMaskButt)
		self.emglistenerbutt.clicked.connect(self.onClickListener)  # regitra EMG y ¿procesa CVMS?
		self.calibbutt.clicked.connect(self.onClickCVMs)  # regitra threshold
		self.emgstopbutt.clicked.connect(self.onClickStopemg)
		self.sendparambutt.clicked.connect(self.onClickSendParamButt)
		
		self.exitbutt2.clicked.connect(self.onClickExitButt)


	#Ui text and value methtods

	def onTextChangedCurrentNum(self, text):
		# print(text)
		self.newcurrent = text


	def onTextChangedFreqNum(self, text):
		# print(text)
		self.newfreq = text


	def onTextChangedPWNum(self, text):
		# print(text)
		self.newpw = text


	def onTextChangedDTNum(self, text):
		# print(text)
		self.newdt = text


	def onTextChangedPNNum(self, text):
		# print(text)
		self.newpn = text
	
	
	def onStateChangedFcheckch1(self, state):
		# print(state == QtCore.Qt.Checked)
		self.check1 = (state == QtCore.Qt.Checked)
	
	
	def onStateChangedFcheckch2(self, state):
		# print(state == QtCore.Qt.Checked)
		self.check2 = (state == QtCore.Qt.Checked)
	
	
	def onStateChangedFcheckch3(self, state):
		# print(state == QtCore.Qt.Checked)
		self.check3 = (state == QtCore.Qt.Checked)
	
	
	def onStateChangedFcheckch4(self, state):
		# print(state == QtCore.Qt.Checked)
		self.check4 = (state == QtCore.Qt.Checked)
	
	
	def onStateChangedFcheckch5(self, state):
		# print(state == QtCore.Qt.Checked)
		self.check5 = (state == QtCore.Qt.Checked)
	
	
	def onStateChangedFcheckch6(self, state):
		# print(state == QtCore.Qt.Checked)
		self.check6 = (state == QtCore.Qt.Checked)
	
	
	def onStateChangedFcheckch7(self, state):
		# print(state == QtCore.Qt.Checked)
		self.check7 = (state == QtCore.Qt.Checked)
	
	
	def onStateChangedFcheckch8(self, state):
		# print(state == QtCore.Qt.Checked)
		self.check8 = (state == QtCore.Qt.Checked)
	
	
	#Building************************************************************easy UI--
	def onTextChangedComNum(self, text):
		# model.getList.get()
		# model.setCurrentPort
		self.numberCOM = text
		#print(self.numberCOM)

	# Initializes port COM comunication with FES device
	def onClickConectarComButt(self):
		print('Abriendo puerto COM')
		if self.numberCOM == 0:
			print("Selecciona el numero de puerto COM que desea usar")
		else:
			self.devices.fesdev.initialize('COM' + self.numberCOM)
	# self.devices.fesdev.initialize('COM4')    #manual port set
	
	# Closes COM port comunication
	def onClickDeConectarComButt(self):
		print('Cerrando puerto COM')
		self.devices.fesdev.closePort()
	
	
	# Initiate FES device
	def onClickfesOnButt(self):
		print('Encendiendo TremUna')
		self.devices.fesdev.startOn()
	
	
	# Shuts down FES device anmd sets mask to 0
	def onClickfesOffButt(self):
		print('Apagando TremUna')
		self.devices.fesdev.setMask(0)
		self.devices.fesdev.shutDown()
	
	
	# sending UI parameters to FES device
	# Probar con sleep para evitar errores de envio
	def onClickCurrentButt(self):
		print("Enviando nuevo valor de corriente a los canales seleccionados")
		if self.fcheckch1.isChecked():
			self.devices.fesdev.setCurrent(1, self.newcurrent)
			self.currentnum_1.setNum(int(self.newcurrent))
		if self.fcheckch2.isChecked():
			self.devices.fesdev.setCurrent(2, self.newcurrent)
			self.currentnum_2.setNum(int(self.newcurrent))
		if self.fcheckch3.isChecked():
			self.devices.fesdev.setCurrent(3, self.newcurrent)
			self.currentnum_3.setNum(int(self.newcurrent))
		if self.fcheckch4.isChecked():
			self.devices.fesdev.setCurrent(4, self.newcurrent)
			self.currentnum_4.setNum(int(self.newcurrent))
		if self.fcheckch5.isChecked():
			self.devices.fesdev.setCurrent(5, self.newcurrent)
			self.currentnum_5.setNum(int(self.newcurrent))
		if self.fcheckch6.isChecked():
			self.devices.fesdev.setCurrent(6, self.newcurrent)
			self.currentnum_6.setNum(int(self.newcurrent))
		if self.fcheckch7.isChecked():
			self.devices.fesdev.setCurrent(7, self.newcurrent)
			self.currentnum_7.setNum(int(self.newcurrent))
		if self.fcheckch8.isChecked():
			self.devices.fesdev.setCurrent(8, self.newcurrent)
			self.currentnum_8.setNum(int(self.newcurrent))
	
	
	# sending UI parameters to FES device
	# Probar con sleep para evitar errores de envio
	def onClickFreqButt(self):
		print("Enviando nuevo valor de frecuencia a los canales seleccionados")
		if self.fcheckch1.isChecked():
			self.devices.fesdev.setFrequency(1, self.newfreq)
			self.freqnum_1.setNum(int(self.newfreq))
		if self.fcheckch2.isChecked():
			self.devices.fesdev.setFrequency(2, self.newfreq)
			self.freqnum_2.setNum(int(self.newfreq))
		if self.fcheckch3.isChecked():
			self.devices.fesdev.setFrequency(3, self.newfreq)
			self.freqnum_3.setNum(int(self.newfreq))
		if self.fcheckch4.isChecked():
			self.devices.fesdev.setFrequency(4, self.newfreq)
			self.freqnum_4.setNum(int(self.newfreq))
		if self.fcheckch5.isChecked():
			self.devices.fesdev.setFrequency(5, self.newfreq)
			self.freqnum_5.setNum(int(self.newfreq))
		if self.fcheckch6.isChecked():
			self.devices.fesdev.setFrequency(6, self.newfreq)
			self.freqnum_6.setNum(int(self.newfreq))
		if self.fcheckch7.isChecked():
			self.devices.fesdev.setFrequency(7, self.newfreq)
			self.freqnum_7.setNum(int(self.newfreq))
		if self.fcheckch8.isChecked():
			self.devices.fesdev.setFrequency(8, self.newfreq)
			self.freqnum_8.setNum(int(self.newfreq))
	
	
	# sending UI parameters to FES device
	# Probar con sleep para evitar errores de envio
	def onClickPWButt(self):
		print("Enviando nuevo valor de PW a los canales seleccionados")
		if self.fcheckch1.isChecked():
			self.devices.fesdev.setPW(1, self.newpw)
			self.pwnum_1.setNum(int(self.newpw))
		if self.fcheckch2.isChecked():
			self.devices.fesdev.setPW(2, self.newpw)
			self.pwnum_2.setNum(int(self.newpw))
		if self.fcheckch3.isChecked():
			self.devices.fesdev.setPW(3, self.newpw)
			self.pwnum_3.setNum(int(self.newpw))
		if self.fcheckch4.isChecked():
			self.devices.fesdev.setPW(4, self.newpw)
			self.pwnum_4.setNum(int(self.newpw))
		if self.fcheckch5.isChecked():
			self.devices.fesdev.setPW(5, self.newpw)
			self.pwnum_5.setNum(int(self.newpw))
		if self.fcheckch6.isChecked():
			self.devices.fesdev.setPW(6, self.newpw)
			self.pwnum_6.setNum(int(self.newpw))
		if self.fcheckch7.isChecked():
			self.devices.fesdev.setPW(7, self.newpw)
			self.pwnum_7.setNum(int(self.newpw))
		if self.fcheckch8.isChecked():
			self.devices.fesdev.setPW(8, self.newpw)
			self.pwnum_8.setNum(int(self.newpw))
	
	
	# sending UI parameters to FES device
	# Probar con sleep para evitar errores de envio
	def onClickDTButt(self):
		print("Enviando nuevo valor de DT a los canales seleccionados")
		if self.fcheckch1.isChecked():
			self.devices.fesdev.setDT(1, self.newdt)
			self.dtnum_1.setNum(int(self.newdt))
		if self.fcheckch2.isChecked():
			self.devices.fesdev.setDT(2, self.newdt)
			self.dtnum_2.setNum(int(self.newdt))
		if self.fcheckch3.isChecked():
			self.devices.fesdev.setDT(3, self.newdt)
			self.dtnum_3.setNum(int(self.newdt))
		if self.fcheckch4.isChecked():
			self.devices.fesdev.setDT(4, self.newdt)
			self.dtnum_4.setNum(int(self.newdt))
		if self.fcheckch5.isChecked():
			self.devices.fesdev.setDT(5, self.newdt)
			self.dtnum_5.setNum(int(self.newdt))
		if self.fcheckch6.isChecked():
			self.devices.fesdev.setDT(6, self.newdt)
			self.dtnum_6.setNum(int(self.newdt))
		if self.fcheckch7.isChecked():
			self.devices.fesdev.setDT(7, self.newdt)
			self.dtnum_7.setNum(int(self.newdt))
		if self.fcheckch8.isChecked():
			self.devices.fesdev.setDT(8, self.newdt)
			self.dtnum_8.setNum(int(self.newdt))

	# sending UI parameters to FES device
	# Probar con sleep para evitar errores de envio
	def onClickPNButt(self):
		print("Enviando nuevo valor de PN a los canales seleccionados")
		if self.fcheckch1.isChecked():
			self.devices.fesdev.setPN(1, self.newpn)
			self.pnnum_1.setNum(int(self.newpn))
		if self.fcheckch2.isChecked():
			self.devices.fesdev.setPN(2, self.newpn)
			self.pnnum_2.setNum(int(self.newpn))
		if self.fcheckch3.isChecked():
			self.devices.fesdev.setPN(3, self.newpn)
			self.pnnum_3.setNum(int(self.newpn))
		if self.fcheckch4.isChecked():
			self.devices.fesdev.setPN(4, self.newpn)
			self.pnnum_4.setNum(int(self.newpn))
		if self.fcheckch5.isChecked():
			self.devices.fesdev.setPN(5, self.newpn)
			self.pnnum_5.setNum(int(self.newpn))
		if self.fcheckch6.isChecked():
			self.devices.fesdev.setPN(6, self.newpn)
			self.pnnum_6.setNum(int(self.newpn))
		if self.fcheckch7.isChecked():
			self.devices.fesdev.setPN(7, self.newpn)
			self.pnnum_7.setNum(int(self.newpn))
		if self.fcheckch8.isChecked():
			self.devices.fesdev.setPN(8, self.newpn)
			self.pnnum_8.setNum(int(self.newpn))
	


	# Manual stimulation defined by the UI mask parameter
	def onClickMaskButt(self):
		print('Stimulating selected channels')
		# self.mask = self.inspectmask()
		maskarade = 0
		if self.fcheckch1.isChecked():
			maskarade += 1
		if self.fcheckch2.isChecked():
			maskarade += 2
		if self.fcheckch3.isChecked():
			maskarade += 4
		if self.fcheckch4.isChecked():
			maskarade += 8
		if self.fcheckch5.isChecked():
			maskarade += 16
		if self.fcheckch6.isChecked():
			maskarade += 32
		if self.fcheckch7.isChecked():
			maskarade += 64
		if self.fcheckch8.isChecked():
			maskarade += 128
		# print(self.mask)
		Ui_Form.devices.fesdev.mask = maskarade
		# return self.mask
		# self.devices.fesdev.stimulation(self.mask)

	lthreader = LThread()
	sthreader = SThread()
	# Start EMG listening process
	def onClickListener(self):

		Ui_Form.lthreader.start()
		Ui_Form.sthreader.start()
		print("Initiating EMG proccesing")
	
	
	#Building	***************************************************************
	def onClickCVMs(self):
		Ui_Form.devices.emgdev.detection_triplethreshold_calibration()
	#Stops EMG listening proccess
	def onClickStopemg(self, threader):
		Ui_Form.lthreader.exit()
		Ui_Form.lthreader.exit()
		print("cierras?")

	#Exit app
	def onClickExitButt(self):
		app.closeAllWindows()
	
	
	#Send UI parameters to FES device
	def onClickSendParamButt(self):
		print("Enviando Parametros a los canales seleccionados")
		if self.fcheckch1.isChecked():
			self.devices.fesdev.setChannels(1, self.newcurrent, self.newfreq, self.newpn, self.newdt, self.newpw)
			self.currentnum_1.setNum(int(self.newcurrent))
			self.freqnum_1.setNum(int(self.newfreq))
			self.pnnum_1.setNum(int(self.newpn))
			self.dtnum_1.setNum(int(self.newdt))
			self.pwnum_1.setNum(int(self.newpw))
		
		if self.fcheckch2.isChecked():
			self.devices.fesdev.setChannels(2, self.newcurrent, self.newfreq, self.newpn, self.newdt, self.newpw)
			self.currentnum_2.setNum(int(self.newcurrent))
			self.freqnum_2.setNum(int(self.newfreq))
			self.pnnum_2.setNum(int(self.newpn))
			self.dtnum_2.setNum(int(self.newdt))
			self.pwnum_2.setNum(int(self.newpw))
		
		if self.fcheckch3.isChecked():
			self.devices.fesdev.setChannels(3, self.newcurrent, self.newfreq, self.newpn, self.newdt, self.newpw)
			self.currentnum_3.setNum(int(self.newcurrent))
			self.freqnum_3.setNum(int(self.newfreq))
			self.pnnum_3.setNum(int(self.newpn))
			self.dtnum_3.setNum(int(self.newdt))
			self.pwnum_3.setNum(int(self.newpw))
		
		if self.fcheckch4.isChecked():
			self.devices.fesdev.setChannels(4, self.newcurrent, self.newfreq, self.newpn, self.newdt, self.newpw)
			self.currentnum_4.setNum(int(self.newcurrent))
			self.freqnum_4.setNum(int(self.newfreq))
			self.pnnum_4.setNum(int(self.newpn))
			self.dtnum_2.setNum(int(self.newdt))
			self.pwnum_4.setNum(int(self.newpw))
		
		if self.fcheckch5.isChecked():
			self.devices.fesdev.setChannels(5, self.newcurrent, self.newfreq, self.newpn, self.newdt, self.newpw)
			self.currentnum_5.setNum(int(self.newcurrent))
			self.freqnum_5.setNum(int(self.newfreq))
			self.pnnum_5.setNum(int(self.newpn))
			self.dtnum_5.setNum(int(self.newdt))
			self.pwnum_5.setNum(int(self.newpw))
		
		if self.fcheckch6.isChecked():
			self.devices.fesdev.setChannels(6, self.newcurrent, self.newfreq, self.newpn, self.newdt, self.newpw)
			self.currentnum_6.setNum(int(self.newcurrent))
			self.freqnum_6.setNum(int(self.newfreq))
			self.pnnum_6.setNum(int(self.newpn))
			self.dtnum_6.setNum(int(self.newdt))
			self.pwnum_6.setNum(int(self.newpw))
		
		if self.fcheckch7.isChecked():
			self.devices.fesdev.setChannels(7, self.newcurrent, self.newfreq, self.newpn, self.newdt, self.newpw)
			self.currentnum_7.setNum(int(self.newcurrent))
			self.freqnum_7.setNum(int(self.newfreq))
			self.pnnum_7.setNum(int(self.newpn))
			self.dtnum_7.setNum(int(self.newdt))
			self.pwnum_7.setNum(int(self.newpw))
		
		if self.fcheckch8.isChecked():
			self.devices.fesdev.setChannels(8, self.newcurrent, self.newfreq, self.newpn, self.newdt, self.newpw)
			self.currentnum_8.setNum(int(self.newcurrent))
			self.freqnum_8.setNum(int(self.newfreq))
			self.pnnum_8.setNum(int(self.newpn))
			self.dtnum_8.setNum(int(self.newdt))
			self.pwnum_8.setNum(int(self.newpw))

	# Auxiliar function to inspect UI mask parameter for FES device
	def inspectmask(self):
		maski = 0
		if self.fcheckch1.isChecked():
			maski += 1
		if self.fcheckch2.isChecked():
			maski += 2
		if self.fcheckch3.isChecked():
			maski += 4
		if self.fcheckch4.isChecked():
			maski += 8
		if self.fcheckch5.isChecked():
			maski += 16
		if self.fcheckch6.isChecked():
			maski += 32
		if self.fcheckch7.isChecked():
			maski += 64
		if self.fcheckch8.isChecked():
			maski += 128
		return maski
	
	
	#  Borrar; usando threads
	def listenert(self):
		# senal = self.emgdev.signal
		# Resolve an available OpenSignals stream
		print("# Looking for an available OpenSignals stream...")
		os_stream = resolve_stream("name", "OpenSignals")
		
		# Create an inlet to receive signal samples from the stream
		inlet = StreamInlet(os_stream[0])
		
		# Get information about the stream
		stream_info = inlet.info()
		
		# Get individual attributes
		stream_name = stream_info.name()
		stream_mac = stream_info.type()
		stream_host = stream_info.hostname()
		stream_n_channels = stream_info.channel_count()
		
		# Store sensor channel info & units in dictionary
		stream_channels = dict()
		channels = stream_info.desc().child("channels").child("channel")
		
		# Loop through all available channels
		for i in range(stream_n_channels - 1):
			# Get the channel number (e.g. 1)
			channel = i + 1
			
			# Get the channel type (e.g. ECG)
			sensor = channels.child_value("sensor")
			
			# Get the channel unit (e.g. mV)
			unit = channels.child_value("unit")
			
			# Store the information in the stream_channels dictionary
			stream_channels.update({channel: [sensor, unit]})
			channels = channels.next_sibling()
		
		while True:
			# Receive samples
			sample, timestamp = inlet.pull_sample()
			
			# print(sample)
			
			if sample is not None:
				self.devices.emgdev.add_sample(samplechunk = sample)
		#  senal.add_sample(samplechunk=sample[0])


#Building*************************************************************************************************************
class BThread(QThread):
	
	def run(self):
		print("building")








if __name__ == "__main__":
	import sys
	
	app = QtWidgets.QApplication(sys.argv)
	Dialog = QtWidgets.QDialog()
	ui = Ui_Form()
	ui.setupUi(Dialog)
	Dialog.show()
	sys.exit(app.exec_())