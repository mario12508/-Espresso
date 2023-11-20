import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, \
    QTableWidgetItem, QLineEdit
from PyQt5.uic import loadUi
import sqlite3


class AddEditCoffeeForm(QDialog):
    def __init__(self, parent=None):
        super(AddEditCoffeeForm, self).__init__(parent)
        loadUi('addEditCoffeeForm.ui', self)
        self.saveButton.clicked.connect(self.save_data)

    def save_data(self):
        # Сохранение данных в базе данных
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()

        # Пример: вставка новой записи
        cursor.execute("INSERT INTO coffee (name, roast_degree, price) "
                       "VALUES (?, ?, ?)",
                       (self.nameLineEdit.text(),
                        self.roastDegreeLineEdit.text(),
                        float(self.priceLineEdit.text())))

        connection.commit()
        connection.close()

        self.accept()  # Закрываем форму после сохранения данных


class CoffeeApp(QMainWindow):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        loadUi('main.ui', self)
        self.loadDataButton.clicked.connect(self.load_data)
        self.addCoffeeButton.clicked.connect(self.show_add_coffee_form)
        self.editCoffeeButton.clicked.connect(self.show_edit_coffee_form)

    def load_data(self):
        connection = sqlite3.connect('coffee.sqlite')
        cursor = connection.cursor()

        # Пример запроса к базе данных
        cursor.execute("SELECT name, roast_degree, price FROM coffee")
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

    def show_add_coffee_form(self):
        form = AddEditCoffeeForm(self)
        if form.exec_() == QDialog.Accepted:
            self.load_data()  # Обновляем данные после добавления

    def show_edit_coffee_form(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row >= 0:
            form = AddEditCoffeeForm(self)
            # Заполняем форму данными из выбранной строки
            for col_num in range(self.tableWidget.columnCount()):
                header_item = self.tableWidget.horizontalHeaderItem(col_num)
                if header_item:
                    line_edit = form.findChild(QLineEdit,
                                               f'{header_item.text()}LineEdit')
                    if line_edit:
                        line_edit.setText(
                            self.tableWidget.item(selected_row,
                                                  col_num).text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())
