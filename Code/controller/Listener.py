# -*- coding: utf-8 -*-

import threading
from pylsl import StreamInlet, resolve_stream
from PyQt5.QtCore import QThread, pyqtSignal
from time import sleep
from model.EMGDevice import signalemg
from view.Appview import *


class LThread(QThread):
	# signaler = pyqtSignal(list)
	# boolean = False

	def run(self):
		# self.senal = signalemg()
		# self.boolean = False
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
			samplei, timestamp = inlet.pull_sample()

			sample = list(samplei)
			# print(samplei)
			try:
				# if sample is not None:
				Ui_Form.devices.emgdev.add_sample(samplechunk=sample[1])
			#  senal.add_sample(samplechunk=sample[0])

			except:
				print(Exception)
			sleep(0.2)
			# print(Ui_Form.devices.emgdev.signal)
			Ui_Form.devices.emgdev.limit_chunk()
			if Ui_Form.devices.emgdev.calibration_threshold != 0:
				print(samplei[1])
				if samplei[1] > Ui_Form.devices.emgdev.calibration_threshold:
					print("llegooooooo")
					# Ui_Form.devices.emgdev.activate_boolean()
					# speakerthread = SThread()
					# speakerthread.run()
					sleep(2)  #Security rest time??????????????????????????????????????????????????????????????????