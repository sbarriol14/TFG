# -*- coding: utf-8 -*-


class signalemg(object):
	def __init__(self):
		self.signal = list()
		self.actfes = False
		self.samplingrate = 1000
		self.calibration_threshold = 0

	def __call__(self):
		self.signal = list()
	
	# Adds a sample to the device signal list
	def add_sample(self, samplechunk):
		self.signal.append(samplechunk)
	
	# Reboots signal list for freeing memory
	def limit_chunk(self):
		if len(self.signal) > 10000000:
			self.signal = list()
			
	# Calibrates threshold for onset detections
	def detection_triplethreshold_calibration(self):
		maxim = abs(max(list(self.signal)))
		self.calibration_threshold = 3*maxim
		print("Threshold: ")
		print(self.calibration_threshold)
		
	# Sets EMG device state to active
	def activate_boolean(self):
		self.actfes = True
	
	# Sets EMG device state to active
	def deactivate_boolean(self):
		self.actfes = False
