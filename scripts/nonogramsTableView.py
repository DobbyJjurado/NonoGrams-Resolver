from PyQt5.QtWidgets import QAbstractItemView,QTableWidget,QTableWidgetItem
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import * 
from PyQt5 import QtCore
import numpy as np
 
class NonoGramsTable(QTableWidget):
	def __init__(self, parent, size:int, data:list = []):
		QTableWidget.__init__(self, parent=parent)
		self._size = size

		if not data:
			self.generateEmptyTable()
		else:
			self._data = data

		self.minimun_size_table = 30
		self.setData()
		self.configureTableView()



	def configureTableView(self) -> None:

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


	def generateEmptyTable(self) -> None:
		self._data = np.eye(self._size, dtype= int)
 
	def setData(self) -> None: 
		self.setRowCount(self._size)
		self.setColumnCount(self._size)

		for n, item in enumerate(self._data):
			for m, item in enumerate(self._data[n]):
				newitem = QTableWidgetItem(item)
				if item == 0:
					newitem.setBackground(QColor(255,255,255))
				else:
					newitem.setBackground(QColor(0,0,0))
				self.setItem(m, n, newitem)
				self.configureWidthHeights()

	
	def configureWidthHeights(self) -> None:
		for i in range(self._size):
			self.setColumnWidth(i, self.minimun_size_table)
			self.setRowHeight(i,self.minimun_size_table)
		
		self.setGeometry(self.minimun_size_table*self._size, self.minimun_size_table*self._size, self.minimun_size_table*self._size, self.minimun_size_table*self._size)


	def update(self, size: int) -> None:
		self.clear()
		self.setRowCount(0)
		self.setColumnCount(0)

		self._size = size
		self.generateEmptyTable()
		self.setData()

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
	main = QWidget()
	main.setMaximumSize(300, 300)
	main.setMinimumSize(300, 300)
	win = NonoGramsTable(main, 2)
	win.update(4)
	main.show()
	sys.exit(app.exec_())