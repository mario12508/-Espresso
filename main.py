import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5.uic import loadUi
import sqlite3


class CoffeeApp(QMainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        loadUi('main.ui', self)
        self.loadDataButton.clicked.connect(self.load_data)

    def load_data(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()

        # Пример запроса к базе данных
        cursor.execute("SELECT * FROM coffee")
        data = cursor.fetchall()

        # Очистка таблицы перед загрузкой новых данных
        self.tableWidget.setRowCount(0)

        # Загрузка данных в QTableWidget
        for row_num, row_data in enumerate(data):
            self.tableWidget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.tableWidget.setItem(row_num, col_num, item)

        connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())
