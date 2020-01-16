# -*- coding: utf-8 -*-

from model.FESDevice import configFES
from model.EMGDevice import signalemg

class Devices(object):
	def __init__(self):
		self.fesdev = configFES()  ## variable inicio objeto dispositivo
		self.emgdev = signalemg()