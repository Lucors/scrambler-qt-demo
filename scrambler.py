# -*- coding: utf-8 -*-
#SYSTEM
import os
import sys
#GUI
from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtWidgets import QGridLayout, QLabel
from PySide2.QtWidgets import QPushButton, QLineEdit
from PySide2.QtCore import Qt, QBitArray

# Класс Скремблера
class Scrambler():
	def __init__(self, scr=0, key=0):
		self.setScr(QBitArray(scr))
		self.setKey(QBitArray(key))

	def reset(self):
		self._tmpKey = QBitArray(self._key)

	def setKey(self, key):
		self._key = key
		self.reset()

	def setScr(self, scr):
		self._scr = scr

	def getKey(self):
		return self._key

	def getScr(self):
		return self._scr

	# Метод сдвига self._tmpKey влево на 1 бит
	def _shiftleft(self, firstBit):
		for i in range(self._tmpKey.size()-1, -1, -1):
			if (i-1 >= 0):
				self._tmpKey.setBit(i, self._tmpKey[i-1])
			else:
				self._tmpKey.setBit(i, firstBit)

	# Метод пошаговой обработки 
	def step(self, inputBit):
		firstBit = None 
		for i in range(self._scr.size()):
			if (self._scr.at(i)):
				if (firstBit == None):
					firstBit = self._tmpKey.at(i)
				else:
					firstBit ^= self._tmpKey.at(i)
		result = [None, None]
		result[1] = self._tmpKey.at(self._tmpKey.size()-1)
		result[0] = inputBit ^ result[1] 
		self._shiftleft(firstBit)
		return result

# Класс визуального интерфейса скремблера
class ScramblerGUI(QWidget):
	def __init__(self, scr=0, key=0):
		super().__init__()
		self.setWindowTitle("GUI Скремблера")
		self._scrambler = Scrambler(scr, key)
		self._layout = QGridLayout(self)

		scrLabel = QLabel("Скремблер:")
		keyLabel = QLabel("Ключ:")
		plainLabel = QLabel("Откр. текст:")
		encryptLabel = QLabel("Зашифр. текст:")
		seqLabel = QLabel("Шифр. послед.:")
		self.scrLE = QLineEdit()
		self.keyLE = QLineEdit()
		self.plainLE = QLineEdit()
		self.encryptLE = QLineEdit()
		self.seqLE = QLineEdit()
		encryptPB = QPushButton("Зашифр.")
		decryptPB = QPushButton("Расшифр.")

		self._layout.addWidget(scrLabel, 0, 0)
		self._layout.addWidget(self.scrLE, 0, 1)
		self._layout.addWidget(keyLabel, 1, 0)
		self._layout.addWidget(self.keyLE, 1, 1)
		self._layout.addWidget(plainLabel, 2, 0)
		self._layout.addWidget(self.plainLE, 2, 1)
		self._layout.addWidget(encryptLabel, 3, 0)
		self._layout.addWidget(self.encryptLE, 3, 1)
		self._layout.addWidget(seqLabel, 4, 0)
		self._layout.addWidget(self.seqLE, 4, 1)
		self._layout.addWidget(encryptPB, 5, 0, 1, 2)
		self._layout.addWidget(decryptPB, 6, 0, 1, 2)

		self.scrLE.editingFinished.connect(self._setScr)
		self.keyLE.editingFinished.connect(self._setKey)
		encryptPB.clicked.connect(self._encryptHandler)
		decryptPB.clicked.connect(self._decryptHandler)
		self.show()

	# Метод перевода строки в QBitArray
	def toBitArray(self, raw):
		result = QBitArray(len(raw))
		for i in range(len(raw)):
			if (raw[i] == '0'):
				result.setBit(i, False)
			else:
				result.setBit(i, True)
		return result

	def _setScr(self):
		self._scrambler.setScr(
			self.toBitArray(self.scrLE.text()))

	def _setKey(self):
		self._scrambler.setKey(
			self.toBitArray(self.keyLE.text()))

	def _encryptHandler(self):
		encrypted = self.encrypt(self.plainLE.text())
		self.encryptLE.setText(encrypted)

	def _decryptHandler(self):
		decrypted = self.encrypt(self.encryptLE.text())
		self.plainLE.setText(decrypted)
		
	# Метод кодирования plainString
	def encrypt(self, plainString):
		result = ""
		sequence = ""
		plain = self.toBitArray(plainString)

		# Циклический вызов Scrambler.step
		for i in range(plain.size()):
			r = self._scrambler.step(plain.at(i))
			result += '1' if r[0] else '0'
			sequence += '1' if r[1] else '0'
		self._scrambler.reset()
		self.seqLE.setText(sequence)
		return result


if __name__ == '__main__':
	app = QApplication(sys.argv)
	scramblerGUI = ScramblerGUI()
	sys.exit(app.exec_())