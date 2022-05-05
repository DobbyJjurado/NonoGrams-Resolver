#!/usr/bin/env python3

from PyQt5.QtWidgets import QAbstractItemView,QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore
import numpy as np

"""
Custom QTableWidget for Nonograms GUI
"""
 
class NonoGramsTable(QTableWidget):

	"""
	
	Customizing QTableWidget for the Nonograms Resolver application. Inherits from QTableWidget

	Attributes:
		size (int, private): Table size. size x size
		data (list, optional): Data to represent in table.
		minimun_size_table (int): Table size. By Default= 30

	"""

	def __init__(self, parent, size:int, data:list = []) -> None:

		"""

		The constructor for NonoGramsTable class.
  
		Parameters:
			parent (QWidget): Parent on which I will display the widget
		   	size (int): NonoGrams table size
		   	data (list, optional): Data to represent in table.
		"""

		QTableWidget.__init__(self, parent=parent)
		self.__size = size

		if not data:
			self.generateEmptyTable()
		else:
			self.__data = data

		self.minimun_size_table = 30
		self.setData()
		self.configureTableView()



	def configureTableView(self) -> None:

		"""

		The function to configure widget.
		
		"""

		# Configure vertical and horizontal Header
		self.verticalHeader().setVisible(False)
		self.verticalHeader().setMinimumSectionSize(self.minimun_size_table)

		self.horizontalHeader().setVisible(False)
		self.horizontalHeader().setMinimumSectionSize(self.minimun_size_table)

		# Configure vertical and Horizontal ScrollBar
		self.verticalScrollBar().setDisabled(True)
		self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.horizontalScrollBar().setDisabled(True)
		self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		
		# Set non editable
		self.setEditTriggers(QTableWidget.NoEditTriggers)

		# No selectable
		self.setSelectionMode(QAbstractItemView.NoSelection)

		# No focus
		self.setFocusPolicy(QtCore.Qt.NoFocus)

	def getData(self) -> list:
		return self.__data

	def generateEmptyTable(self) -> None:

		"""
		The function to generate matrix with size -> self.size.

		>>> table.generateEmptyTable()
		>>> table.getData()
		array([[0, 0, 0],
		       [0, 0, 0],
		       [0, 0, 0]])

		"""

		self.__data = np.zeros((self.__size, self.__size),dtype= int)
 
	def setData(self) -> None: 
		"""

		Function to generate the cells and paint them white if the element contains the value 0, 
		otherwise they will be painted black.
		
		"""

		self.setRowCount(self.__size)
		self.setColumnCount(self.__size)

		for n, item in enumerate(self.__data):
			for m, item in enumerate(self.__data[n]):
				newitem = QTableWidgetItem(item)
				if item == 0:
					newitem.setBackground(QColor(255,255,255))
				else:
					newitem.setBackground(QColor(0,0,0))
				self.setItem(m, n, newitem)
				self.configureWidthHeights()

	
	def configureWidthHeights(self) -> None:
		"""

		Function to configure the size of the cells. This size is indicated by the minimun_size_table parameter.

		"""
		for i in range(self.__size):
			self.setColumnWidth(i, self.minimun_size_table)
			self.setRowHeight(i,self.minimun_size_table)
		
		self.setGeometry(self.minimun_size_table*self.__size, self.minimun_size_table*self.__size, self.minimun_size_table*self.__size, self.minimun_size_table*self.__size)


	def update(self, size: int) -> None:
		"""
		
		Function to generate a new table. 

		Parameters:
			size (int): New Size.

		>>> table.update(4)
		>>> table.getData()
		array([[0, 0, 0, 0],
		       [0, 0, 0, 0],
		       [0, 0, 0, 0],
		       [0, 0, 0, 0]])

		>>> table.update(3)
		>>> table.getData()
		array([[0, 0, 0],
		       [0, 0, 0],
		       [0, 0, 0]])

		"""
		self.clear()
		self.setRowCount(0)
		self.setColumnCount(0)

		self.__size = size
		self.generateEmptyTable()
		self.setData()

if __name__ == "__main__":

	import doctest
	import sys

	
	app = QApplication(sys.argv)
	main = QWidget()
	"Test with size 3"
	doctest.testmod(extraglobs={'table': NonoGramsTable(main,size=3)})

	"""
	import sys
	app = QApplication(sys.argv)
	main = QWidget()
	main.setMaximumSize(300, 300)
	main.setMinimumSize(300, 300)
	win = NonoGramsTable(main, 2)
	win.update(4)
	main.show()
	sys.exit(app.exec_())
	"""