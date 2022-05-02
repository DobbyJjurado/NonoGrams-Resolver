from PyQt5.QtWidgets import QApplication,QLineEdit,QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from re import match
from PyQt5.QtWidgets import QMessageBox


class nonoGramsLineEdit(QLineEdit):
	def __init__(self,parent, size: int, width:int = 50, height:int = 15):
		QLineEdit.__init__(self, parent=parent)
		self._size = size
		self.data = ""
		self.width = width
		self.height = height

		self.connectSignals()
		self.configure()


	def connectSignals(self):
		self.textChanged.connect(self.textSignal)

	def configure(self):
		self.setAlignment(Qt.AlignCenter)
		self.setFont(QFont("Arial", 7, QFont.ExtraBold))
		self.setFixedWidth(self.width)
		self.setFixedHeight(self.height)

	def textSignal(self,text):
		if match("^[0-9 ]+$", text):
			num_list = [int(i) for i in text.split(" ") if  i != ""]
			if sum(num_list) <=  self._size:
				self.data = num_list
			else:
				QMessageBox.about(self, "Error", "The sum of the numbers entered is greater than the size of the nonogram.")
				print(text[:-1])
				self.setText(text[:-1])
		else:
			self.clear()

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	main = QWidget()
	main.setMaximumSize(150, 150)
	main.setMinimumSize(150, 150)
	win = nonoGramsLineEdit(main, 2)
	main.show()
	sys.exit(app.exec_())