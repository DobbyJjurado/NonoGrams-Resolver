from PyQt5.QtWidgets import QApplication,QLineEdit,QWidget
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
from re import match
from PyQt5.QtWidgets import QMessageBox

"""
Custom QLineEdit for Nonograms GUI
"""


class nonoGramsLineEdit(QLineEdit):

	"""
	
	Customizing QLineEdit for the Nonograms Resolver application. Inherits from QLineEdit

	Attributes:
		data (str): Data entered by the user.
		width (int, optional): Widget width
		height (int, optional): Widget heigth
		size (int, private): NonoGrams Size

	"""

	def __init__(self,parent, size: int, width:int = 50, height:int = 15) -> None:

		"""

		The constructor for nonoGramsLineEdit class.
  
		Parameters:
		   parent (QWidget): Parent on which I will display the widget
		   size (int): NonoGrams Size
		   width (int): Widget width
		   height (int):  Widget heigth 
		"""

		QLineEdit.__init__(self, parent=parent)
		self.__size = size
		self.data = []
		self.width = width
		self.height = height

		self.connectSignals()
		self.configure()


	def connectSignals(self) -> None:
	
		"""

		The function to connect widget signals.

		"""

		self.textChanged.connect(self.textSignal)

	def configure(self) -> None:
		"""

		The function to configure widget.
		
		"""

		self.setAlignment(Qt.AlignCenter)
		self.setFont(QFont("Arial", 7, QFont.ExtraBold))
		self.setFixedWidth(self.width)
		self.setFixedHeight(self.height)

	def textSignal(self, text: str) -> None:

		"""

		Function that makes sure that the text entered is only numbers and 
		that the total of the numbers entered does not exceed the value of the size.

		Parameters:
			text (str): String to check.

		>>> line_edit.textSignal("Hola Que tal")
		>>> line_edit.data
		[]

		>>> line_edit.textSignal("4")
		>>> line_edit.data
		[4]

		>>> line_edit.textSignal("2 2")
		>>> line_edit.data
		[2, 2]

		>>> line_edit.textSignal("1 1 2")
		>>> line_edit.data
		[1, 1, 2]

		>>> line_edit.textSignal("5 12")
		>>> line_edit.data
		[5]

		>>> line_edit.textSignal("Juan")
		>>> line_edit.data
		[]
		
		
		"""
		if match("^[0-9 ]+$", text):
			num_list = [int(i) for i in text.split(" ") if  i != ""]
			if sum(num_list) <=  self.__size:
				self.data = num_list
			else:
				if __name__ != "__main__": QMessageBox.about(self, "Error", "The sum of the numbers entered is greater than the size of the nonogram.")
				self.setText(text[:-1])
				self.data = num_list[:-1]
		else:
			self.clear()
			self.data.clear()

if __name__ == "__main__":
	import doctest
	import sys

	
	app = QApplication(sys.argv)
	main = QWidget()
	"Test with size 5"
	doctest.testmod(extraglobs={'line_edit': nonoGramsLineEdit(main,size=5)})

	"""
	app = QApplication(sys.argv)
	main = QWidget()
	main.setMaximumSize(150, 150)
	main.setMinimumSize(150, 150)
	win = nonoGramsLineEdit(main, 2)
	main.show()
	sys.exit(app.exec_())
	"""