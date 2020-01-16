# -*- coding: utf-8 -*-


class Channel(object):
    # PW, DT, PN array of two bytes (intervales)
    def __init__(self):
        self._isActive = False
        self._I = 0
        self._I = bytes([self._I])
        self._f = 0
        self._f = bytes([self._f])
        self._PW = bytes([0, 250])
        self._DT = bytes([0, 0])
        self._PN = bytes([0, 0])

    # Initialize with predefined parameters;  PW, DT, PN array of two bytes (intervales)
    def initialize(self, isActive, I, f, PW, PN, DT):
        self._isActive = isActive
        self._I = I.tobyte()
        self._f = f.tobyte()
        self._PW = PW.tobytes()
        self._DT = DT.tobytes()
        self._PN = PN.tobytes()

    # Parameter setters for the channel
    def setActive(self, isActive):
        self._isActive = isActive

    def setI(self, I):
        # self._I = bytes([I])
        self._I = I

    def setf(self, f):
        self._f = f

    def setPW(self, PW):
        self._PW = [0, PW]

    def setPN(self, PN):
        self._PN = [0, PN]

    def setDT(self, DT):
        self._PN = [0, DT]
        
    #Parameter getters for the channel

    def getI(self):
        return self._I

    def getf(self):
        return self._f

    def getPW(self):
        return self._PW[1]

    def getDT(self):
        return self._DT[1]

    def getPN(self):
        return self._PN[1]
