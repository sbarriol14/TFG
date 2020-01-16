# -*- coding: utf-8 -*-
"""
Created on Wed Feb  6 13:38:42 2019

@author: toz30
"""

from .Channel import Channel  # import markerFES
import serial
from time import sleep


class configFES(object):
	def __init__(self):
		# BaudRate
		self._BR230400 = 230400
		self._BR460800 = 460800
		self._BR500000 = 500000
		self._BR576000 = 576000
		self._BR921600 = 921600
		self._BR1000000 = 1000000
		self._ceros = 0
		self._b62 = bytes([62])
		self._Channels = []
		# init serial COM
		self._serialPort = serial.Serial()
		self.binarymask = ''
		self.mask = 0

	#Initialices port comunication of TremUna
	# (Optim?)
	def initialize(self, port):
		# init channels
		i = 0
		while i < 8:
			canal = Channel()
			self._Channels.append(canal)
			i += 1
		# CONFIGURATION
		configuration_status = self.setPort(port)
		if configuration_status == 1:
			print("\n" + port + " selectioned")
		else:
			print(port + ": error in port selection")
		# CONEXION
		conection_status = self._serialPort.isOpen()
		if conection_status:
			print(port + " open")
		else:
			print(port + ": is not open")
			self._serialPort.open()

	# Turn On TremUna
	def startOn(self):

		stim_param_pckt = ">ON<"
		stim_param_pcktbb = bytes(stim_param_pckt, 'utf8')

		ack = [self._ceros, self._ceros, self._ceros, self._ceros, self._ceros]
		print("\n" + stim_param_pckt)
		# send ON
		try:
			self._serialPort.write(stim_param_pcktbb)
		except serial.SerialException:
			print("Start ON: Write SerialPort Err")

		# read ACK
		i = 0
		while i < 4:    # nose porque no me funciona con 5...entra en bucle
			try:
				ack[i] = self._serialPort.read()
				ack[i] = int.from_bytes(ack[i], byteorder="little")
				i += 1
			except serial.SerialException:
				print("Start ON: Read SerialPort Err")

		if (ack[0] == 62) and (ack[1] == 69):
			print("Start ON: Can't reach TREMUNA device")

	#Turn Off TremUna
	def shutDown(self):        # ShutdownFES
		stim_param_pckt = ">OFF<"
		stim_param_pcktbb = bytes(stim_param_pckt, 'utf8')
		ack = [self._ceros, self._ceros, self._ceros, self._ceros, self._ceros]
		print("\n" + stim_param_pckt)
		try:   # send OFF
			self._serialPort.write(stim_param_pcktbb)
		except serial.SerialException:
			print("Shut down: write failed!")
		finally:
			i = 0
			while i < 4:   # read ACK
				try:
					ack[i] = self._serialPort.read(1)
					ack[i] = int.from_bytes(ack[i], byteorder="little")
					i += 1

				except serial.SerialException:
					print("Shut down: read failed!")
		if (ack[0] == 62) and (ack[1] == 69):
			print("Shutdown failed!")

	# change Mask to define active or inactive channels
	# newMask is a byte where each position represents the active/inactive state of an electrode.
	# Eg- 0b00000101 or int(5) activates only the electrodes 1 and 3
	def setMask(self, newmask):                             #  no funciona para canala 8, nose poorque no traduce envia bien el mensaje cuando este esta incluido
		self.binarymask = '{0:08b}'.format(newmask)
		# print(self.binarymask[1:2])
		# print(self.binarymask[0:1])
		i = 8
		j = 0
		while i > 0:
			if self.binarymask[(i-1):i] == '1':
				canal = self._Channels[j]
				canal.setActive(True)
			else:
				canal = self._Channels[j]
				canal.setActive(False)
			j += 1
			i -= 1
		newmask = chr((int(newmask)))
		stim_param_pckt = ">SA;" + newmask + "<"
		ack = [self._ceros, self._ceros, self._ceros, self._ceros]
		msg = bytes(stim_param_pckt, 'utf8')
		try:   # send
			self._serialPort.write(msg)
		except serial.SerialException:
			print("write failed!")
		finally:
			i = 0
			while i < 4:   # read ACK
				try:
					ack[i] = self._serialPort.read(1)
					ack[i] = int.from_bytes(ack[i], byteorder="little")
					i += 1
				except serial.SerialException:
					print("read failed!")
		if (ack[0] == 62) and (ack[1] == 69):
			print("Mask set failed!")

	# Set the current to the specified channel
	def setCurrent(self, ch2s, newcurrent):
		canal = self._Channels[ch2s-1]
		newcurrentb = bytes(newcurrent, 'utf8')
		canal.setI(newcurrentb)
		self._Channels[ch2s-1] = canal
		ack = [self._ceros, self._ceros, self._ceros, self._ceros]
		ch2s = str(ch2s)
		newcurrent = chr(int(newcurrent))
		msg = ">C" + ch2s + ";" + newcurrent + "<"
		msg = bytes(msg, 'utf8')
		try:   # send
			self._serialPort.write(msg)
		except serial.SerialException:
			print("write failed!")
		finally:
			i = 0
			while i < 4:  # nose porque no me funciona con 5...entra en bucle
				try:
					ack[i] = self._serialPort.read(1)
					ack[i] = int.from_bytes(ack[i], byteorder="little")
					i += 1
				except serial.SerialException:
					print("Start ON: Read SerialPort Err")
		if (ack[0] == 62) and (ack[1] == 69):
			print("Current set failed!")

	# Set frequency to the specified channel
	def setFrequency(self, ch2s, newfreq):
		canal = self._Channels[ch2s-1]
		newfreqb = bytes(newfreq, 'utf8')
		canal.setI(newfreqb)
		self._Channels[ch2s-1] = canal
		ch2s = str(ch2s)
		newfreq = chr(int(newfreq))
		ack = [self._ceros, self._ceros, self._ceros, self._ceros]
		msg = ">F" + ch2s + ";" + newfreq + "<"
		msg = bytes(msg, 'utf8')
		try:   # send
			self._serialPort.write(msg)
		except serial.SerialException:
			print("write failed!")
		finally:
			i = 0
			while i < 4:   # read ACK
				try:
					ack[i] = self._serialPort.read(1)
					ack[i] = int.from_bytes(ack[i], byteorder="little")
					i += 1
				except serial.SerialException:
					print("read failed!")
		if (ack[0] == 62) and (ack[1] == 69):
			print("Frequency set failed!")

	# Set pulse width to the specified channel
	# newPW array of two bytes
	def setPW(self, ch2s, newPW):
		canal = self._Channels[ch2s-1]
		newpwb = bytes(newPW, 'utf8')
		canal.setPW(newpwb)
		self._Channels[ch2s-1] = canal
		ack = [self._ceros, self._ceros, self._ceros, self._ceros]
		ch2s = str(ch2s)
		newPW = chr(int(newPW))
		msg = ">W" + ch2s + ";0" + newPW + "<"
		msg = bytes(msg, 'utf8')
		# print(msg)
		try:  # send
			self._serialPort.write(msg)
		except serial.SerialException:
			print("write failed!")
		finally:
			i = 0
			while i < 4:  # read ACK
				try:
					ack[i] = self._serialPort.read(1)
					ack[i] = int.from_bytes(ack[i], byteorder="little")
					i += 1
				except serial.SerialException:
					print("read failed!")
		if (ack[0] == 62) and (ack[1] == 69):
			print("PW set failed!")

	# Sets the delay time to the specified channel
	# newDT array of two bytes
	def setDT(self, ch2s, newDT):
		canal = self._Channels[ch2s-1]
		newdtb = bytes(newDT, 'utf8')
		canal.setPW(newdtb)
		self._Channels[ch2s-1] = canal
		ack = [self._ceros, self._ceros, self._ceros, self._ceros]
		ch2s = str(ch2s)
		newDT = chr(int(newDT))
		msg = ">D" + ch2s + ";0" + newDT + "<"
		msg = bytes(msg, 'utf8')
		try:   # send
			self._serialPort.write(msg)
		except serial.SerialException:
			print("write failed!")
		finally:
			i = 0
			while i < 4:   # read ACK
				try:
					ack[i] = self._serialPort.read()
					ack[i] = int.from_bytes(ack[i], byteorder="little")
					i += 1
				except serial.SerialException:
					print("read failed!")
		if (ack[0] == 62) and (ack[1] == 69):
			print("DT set failed!")

	# Set pulse number for specified channel
	# newPN array of two bytes
	def setPN(self, ch2s, newPN):
		# canal = Channel()
		canal = self._Channels[ch2s-1]
		newpnb = bytes(newPN, 'utf-8')
		canal.setPW(newpnb)
		self._Channels[ch2s-1] = canal
		ack = [self._ceros, self._ceros, self._ceros, self._ceros]
		ch2s = str(ch2s)
		newPN = chr(int(newPN))
		msg = ">N" + ch2s + ";0" +newPN + "<"
		msg = bytes(msg, 'utf8')
		try:   # send
			self._serialPort.write(msg)
		except serial.SerialException:
			print("write failed!")
		finally:
			i = 0
			while i < 4:   # read ACK
				try:
					ack[i] = self._serialPort.read(1)
					ack[i] = int.from_bytes(ack[i], byteorder="little")
					i += 1
				except serial.SerialException:
					print("read failed!")
		if (ack[0] == 62) and (ack[1] == 69):
			print("PN set failed!")

	# updates the specified channel parameters
	# PW,PN,DT two position bytes arrays (intervales?Optim?)
	def setChannels(self, ch2s, f, current, PN, DT, PW):
		self.setCurrent(ch2s, current)
		self.setFrequency(ch2s, f)
		self.setDT(ch2s, DT)
		self.setPN(ch2s, PN)
		self.setPW(ch2s, PW)

	# Sets and shows the set of parameters of the channels
	def getParameters(self, ch2s):
		setparam = [self._ceros, self._ceros, self._ceros, self._ceros, self._ceros]
		setparam[0] = self._Channels[ch2s].getf()
		setparam[1] = self._Channels[ch2s].getI()
		setparam[2] = self._Channels[ch2s].getPN()
		setparam[3] = self._Channels[ch2s].getDT()
		setparam[4] = self._Channels[ch2s].getPW()
		return setparam

	# Sets the specified port and returns 1 if succesfully
	def setPort(self, portname):
		# param CharParity indicates the number of bits in the transm. "8N1"
		port = portname
		parity = serial.PARITY_NONE
		data_bits = serial.EIGHTBITS
		stop_bits = serial.STOPBITS_ONE
		inter_byte_timeout = 0.1
		write_timeout = 100
		try:
			self._serialPort = serial.Serial(port, self._BR500000,data_bits, parity, stop_bits, timeout=write_timeout,interCharTimeout=inter_byte_timeout)
			return 1
		except serial.SerialException:
			return 0

	# Closes the port and returns 1 if succesfully
	def closePort(self):
		try:
			if self._serialPort.isOpen():
				self._serialPort.close()
				print("\nPort Closed")
			else:
				print("\nPort error")
			return 1  # Success
		except serial.SerialException:
			return 0  # Failure

	# Auxiliar function for stimulation, uses mask
	def stimulation(self, mask):
		if mask != 0:
			self.setMask(mask)
			sleep(1)
			self.setMask(0)
		else:
			print("No hay ningún canal seleccionado")
			self.setMask(0)

	# Opens the port and returns 1 if succesfully
	def openPort(self):
		try:
			print(self._serialPort.isOpen())
			self._serialPort.open()
			return 1   # Success
		except serial.SerialException:
			return 0   # Failure

	# Reading/No use
	def read(self):
		try:
			message = self._serialPort.readline()
			print(message)
		except RuntimeError:
			print("Read Failure")



