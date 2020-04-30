

from PyQt5 import QtCore, QtGui, QtWidgets
import pyodbc as mdb
import ast

arrTables = ['SELECT * FROM dbo.press400',
             'SELECT * FROM dbo.press600',
             'SELECT * FROM dbo.press250Prog',
             'SELECT * FROM dbo.press250Servo',
             'SELECT * FROM dbo.pressAIDA1600',
             'SELECT * FROM dbo.pressAIDA1000']


def MyConverter(mydata):
    def cvt(data):
        try:
            return ast.literal_eval(data)
        except Exception:
            return str(data)
    return tuple(map(cvt, mydata))


class Ui_MainWindow(object):


    def addTable(self, columns):
        rowPosition = self.tableWidget.rowCount()
        self.tableWidget.insertRow(rowPosition)

        for i, column in enumerate(columns):
            self.tableWidget.setItem(rowPosition, i, QtWidgets.QTableWidgetItem(str(column)))

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 743)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(12, 72, 941, 561))
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(12)
        self.tableWidget.setObjectName("tableWidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.clicked.connect(self.LoadData)
        self.pushButton.setGeometry(QtCore.QRect(410, 650, 93, 28))
        self.pushButton.setObjectName("pushButton")

        self.CBox = QtWidgets.QComboBox(self.centralwidget)
        self.CBox.setGeometry(QtCore.QRect(963, 72, 181, 21))
        self.CBox.setObjectName("comboBox")
        self.CBox.addItem('Press400')
        self.CBox.addItem('Press600')
        self.CBox.addItem('Press250Prog')
        self.CBox.addItem('Press250Servo')
        self.CBox.addItem('PressAida1600')
        self.CBox.addItem('PressAida1000')
        self.CBox.currentIndex()

        #self.QBox.currentIndexChanged.connect(self.selectionchange)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 967, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def LoadData(self, orderTable):

        db = mdb.connect('Driver={SQL Server};'
                          'Server=10.18.16.153;'
                         'Database=press_data_control;'
                         'uid=press_spvz; '
                         'pwd=admin100;')

        with db:

            cur = db.cursor()
            rows = cur.execute(arrTables[self.CBox.currentIndex()])
            data = cur.fetchall()
            desc = cur.description


            self.tableWidget.setRowCount(0)
            self.addTable(desc)
            for row in data:
                self.addTable(MyConverter(row))
            cur.close()


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "LoadData"))


if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())

