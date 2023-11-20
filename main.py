import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, \
    QTableWidgetItem, QLineEdit
import sqlite3
from UI.addEditCoffeeForm import Ui_AddEditCoffeeForm
from UI.main import Ui_CoffeeApp


class AddEditCoffeeForm(QDialog, Ui_AddEditCoffeeForm):
    def __init__(self, parent=None):
        super(AddEditCoffeeForm, self).__init__(parent)
        self.setupUi(self)
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


class CoffeeApp(QMainWindow, Ui_CoffeeApp):
    def __init__(self):
        super(CoffeeApp, self).__init__()
        self.ui = Ui_CoffeeApp()
        self.ui.setupUi(self)

        self.ui.loadDataButton.clicked.connect(self.load_data)
        self.ui.addCoffeeButton.clicked.connect(self.show_add_coffee_form)
        self.ui.editCoffeeButton.clicked.connect(self.show_edit_coffee_form)

    def load_data(self):
        connection = sqlite3.connect('data/coffee.sqlite')
        cursor = connection.cursor()

        # Пример запроса к базе данных
        cursor.execute("SELECT name, roast_degree, price FROM coffee")
        data = cursor.fetchall()

        # Очистка таблицы перед загрузкой новых данных
        self.ui.tableWidget.setRowCount(0)

        # Загрузка данных в QTableWidget
        for row_num, row_data in enumerate(data):
            self.ui.tableWidget.insertRow(row_num)
            for col_num, col_data in enumerate(row_data):
                item = QTableWidgetItem(str(col_data))
                self.ui.tableWidget.setItem(row_num, col_num, item)

        connection.close()

    def show_add_coffee_form(self):
        form = AddEditCoffeeForm(self)
        if form.exec_() == QDialog.Accepted:
            self.load_data()  # Обновляем данные после добавления

    def show_edit_coffee_form(self):
        selected_row = self.ui.tableWidget.currentRow()
        if selected_row >= 0:
            form = AddEditCoffeeForm(self)
            # Заполняем форму данными из выбранной строки
            for col_num in range(self.ui.tableWidget.columnCount()):
                form.findChild(QLineEdit, f'''
{self.ui.tableWidget.horizontalHeaderItem(col_num).text()}LineEdit''') \
                    .setText(
                    self.ui.tableWidget.item(selected_row, col_num).text())
            if form.exec_() == QDialog.Accepted:
                self.load_data()  # Обновляем данные после редактирования


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CoffeeApp()
    window.show()
    sys.exit(app.exec_())
