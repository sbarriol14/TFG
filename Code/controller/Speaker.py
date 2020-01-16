# -*- coding: utf-8 -*-

from PyQt5.QtCore import QThread


# from view.vistaFES import Ui_Dialog    no se porque no me deja importar vista

class SThread(QThread):
	
	def run(self):
		print("hola")
	
	while True:
		if Ui_Dialog.devices.emgdev.actfes:
			Ui_Dialog.devices.fesdev.stimulation(Ui_Dialog.inspectmask())
			Ui_Dialog.devices.emgdev.actfes = False