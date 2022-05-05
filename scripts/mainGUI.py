#!/usr/bin/env python3

# importing libraries
from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import * 
import rospy
import sys
from nonogramsTableView import NonoGramsTable
from nonogramsLineEdit import nonoGramsLineEdit
from nonograms_solver.srv import Solution
from std_msgs.msg import String


def nextData(data: list) -> str:
    for i in data:
        yield i

class SecondWindow(QMainWindow):
    dataSendSignal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(SecondWindow, self).__init__(parent)
        self.__width = 300
        self.__height = 450
        self.configure()
        self.initUI()

    def configure(self) -> None:
        self.setMaximumSize(self.__width, self.__height)
        self.setMinimumSize(self.__width, self.__height)
    
    def initUI(self) -> None:

        self.text_edit = QTextEdit(self)
        self.text_edit.resize(self.__width,self.__height - 50)

        self.update_button = QPushButton("Update", self)
        self.update_button.move(int((self.__width - self.update_button.width()) / 2),
                                self.__height - self.update_button.height())
        self.update_button.clicked.connect(self.sendData)

    def sendData(self) -> None:

        self.dataSendSignal.emit(self.text_edit.toPlainText())
        self.close()
        

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        rospy.init_node('gui_node')

        self.spacing = 20
        self.size = 1
        self.column_data = []
        self.row_data = []
        self.data_to_send = []
        self.configure()
        self.rosConfiguration()
        self.UiComponents()
        self.show()

    def rosConfiguration(self):

        self.srv_solver = rospy.ServiceProxy('solver', Solution)
        self.sub_error = rospy.Subscriber("error", String, self.errorCallback)
        
    def configure(self):
        screen = QDesktopWidget().screenGeometry()
        self.width, self.height = screen.size().width() - 450, screen.size().height() - 150
        self.setMaximumSize(self.width, self.height)
        self.setMinimumSize(self.width, self.height)
        self.setWindowTitle('Nonograms Resolver App')
        self.setWindowIcon(QIcon('icon.png'))        


    def UiComponents(self):

        self.label_spin_size = QLabel("NonoGrams Size: ", self)
        self.label_spin_size.move(int(self.frameGeometry().width()/2 - + self.label_spin_size.size().width()),
                                  self.spacing + 5)

        self.spin_size = QSpinBox(self)
        self.spin_size.move(int(self.frameGeometry().width()/2 + self.label_spin_size.size().width() /2 + self.spacing),
                            self.spacing)
        self.spin_size.setMinimum(1)
        self.spin_size.setMaximum(20)
        self.spin_size.valueChanged.connect(self.show_result)
    
        self.nonograms_view = NonoGramsTable(self, self.spin_size.value())
        self.moveTableToCenter()

        self.button_send = QPushButton("Resolve", self)
        self.button_send.move(int(self.frameGeometry().width()/2 - self.button_send.width()/2),
                            int(self.height - self.spacing -self.button_send.height()/2))
        self.button_send.clicked.connect(self.sendDataToSolver)

        self.fill_with_text = QPushButton("Fill with Text", self)
        self.fill_with_text.move(self.button_send.x() + self.button_send.width(),
                              self.button_send.y())
        self.fill_with_text.clicked.connect(self.inputTextData)

        self.window_input_data = SecondWindow(self)
        self.window_input_data.dataSendSignal.connect(self.dataReceivedFromInputDataWindow)

        self.generateInputToNonograms()

    def inputTextData(self) -> None:
        self.window_input_data.show()

    def dataReceivedFromInputDataWindow(self,string)-> None:

        data = string.split("\n")
        generator = nextData(data)
        self.spin_size.setValue(int(next(generator)))

        for i in self.row_data:
            i.setText(next(generator))

        for i in self.column_data:
            i.setText(next(generator))

    def sendDataToSolver(self) -> None:

        self.data_to_send.clear()

        self.data_to_send.append(self.size)
        [self.data_to_send.append([int(x) for x in i.data] ) for i in self.row_data if len(i.data) != 0]
        [self.data_to_send.append([int(x) for x in i.data] ) for i in self.column_data if len(i.data) != 0]

        total_length = self.size * 2 + 1
        current_length = len(self.data_to_send)
        if total_length == current_length:
            print(self.data_to_send)
            self.srv_solver(self.data_to_send)
        else:
            QMessageBox.about(self, "Error", "Missing Data.")


    def show_result(self)-> None:
        # getting current value
        self.size = self.spin_size.value()
        self.nonograms_view.update(self.size)
        self.moveTableToCenter()
        self.generateInputToNonograms()
      

    def moveTableToCenter(self) -> None:

        center_point = self.rect().center()
        x_center  = center_point.x() - int((self.size * self.nonograms_view.minimun_size_table) / 2)
        y_center =  center_point.y() - int((self.size * self.nonograms_view.minimun_size_table) / 2)
        self.nonograms_view.move(x_center, y_center)
                                
    def generateInputToNonograms(self) -> None:

        if self.column_data: 
            [column.deleteLater() for column in self.column_data]
            self.column_data.clear()
        if self.row_data: 
            [row.deleteLater() for row in self.row_data]
            self.row_data.clear()

        center_point = self.rect().center()
        x_center  = center_point.x() - int((self.size * self.nonograms_view.minimun_size_table) / 2)
        y_center =  center_point.y() - int((self.size * self.nonograms_view.minimun_size_table) / 2)

        # Row Data
        for i in range(self.size):
            line_edit = nonoGramsLineEdit(self, self.size,  width = 40, height= self.nonograms_view.minimun_size_table)
            line_edit.move(x_center - line_edit.width, y_center + (i * line_edit.height))
            line_edit.show()
            self.column_data.append(line_edit)

        # Column Data
        for i in range(self.size):
            line_edit = nonoGramsLineEdit(self, self.size, width = self.nonograms_view.minimun_size_table, height= 25)
            line_edit.move(x_center + (i * line_edit.width) , y_center - line_edit.height)
            line_edit.show()
            self.row_data.append(line_edit)

    def errorCallback(self, msg: String):
        QMessageBox.about(self, "Error", msg.data)
 
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_()) 