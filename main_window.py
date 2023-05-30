import json
import multiprocessing as mp
import sys
import time

from PyQt5 import QtWidgets
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtWidgets import (QApplication, QFormLayout, QLabel, QMainWindow,
                             QProgressBar, QPushButton, QSizePolicy,
                             QSpacerItem, QSpinBox, QVBoxLayout, QWidget)

from charting import charting
from hash import algorithm_luna, check_hash


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.folderpath = ""
        while self.folderpath == "":
            self.folderpath = QtWidgets.QFileDialog.getExistingDirectory(
                self, 'select folder with json file')
        with open(f"{self.folderpath}/setting.json", "r") as f:
            self.setting = json.load(f)
        self.setWindowTitle('Search and check card number')
        self.resize(512, 512)
        self.setStyleSheet("background-image: url(background.jpg);")
        self.info_card = QLabel(
            f'Available card information: {self.setting["initial_digits"]}******{self.setting["last_digits"]}')
        layout = QVBoxLayout()
        self.pbar = QProgressBar(self)
        self.pbar.setValue(0)
        self.pbar.hide()
        self.timer = QBasicTimer()
        self.timer.stop()
        title_slider = QLabel('Select number of cores:', self)
        self.result_label = QLabel('Result:')
        layout = QFormLayout()
        self.setLayout(layout)
        spin_box = QSpinBox(self)
        spin_box.setRange(0, 64)
        spin_box.setValue(36)
        spin_box.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.value = spin_box.value()
        self.start_button = QPushButton('To start searching')
        self.start_button.clicked.connect(self.find_solution)
        self.charting_button = QPushButton('Draw a graph')
        self.charting_button.clicked.connect(self.draw_graph)
        layout.addRow(self.info_card)
        layout.addItem(QSpacerItem(
            0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addRow(title_slider)
        layout.addRow(spin_box)
        layout.addRow(self.result_label)
        layout.addRow(self.pbar)
        layout.addWidget(self.start_button)
        layout.addItem(QSpacerItem(
            0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding))
        layout.addRow(self.charting_button)
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def search_card_number(self, start: float) -> None:
        """функция для поиска номера карты

        Args:
            start (float): время начала поиска
        """
        with mp.Pool(self.value) as p:
            for i, result in enumerate(p.map(check_hash, range(99999, 10000000))):
                if result:
                    self.update_pb(start, result)
                    p.terminate()
                    break
                self.update_pb_on_progress(i)
            else:
                self.result_label.setText('Solution not found')
                self.pbar.setValue(100)

    def find_solution(self) -> None:
        """функция подготавливает progressbar, задает время начала и вызывает функцию поиска номера карты
        """
        self.prepare_pb()
        start = time.time()
        self.search_card_number(start)

    def prepare_pb(self) -> None:
        """функция устанавливает начальное значение для progressbar и выводит начальную информацию
        """
        self.result_label.setText('Search in progress...')
        self.pbar.show()
        if not self.timer.isActive():
            self.timer.start(100, self)
        QApplication.processEvents()

    def update_pb(self, start: float, result: float) -> None:
        """функция для обновляет progressbar и вывода информации о карте

        Args:
            start (float): время начала
            result (float): время окончания поиска
        """
        self.pbar.setValue(100)
        end = time.time() - start
        result_text = f'Found: {result}\n\n'
        result_text += f'Checking the Luhn Algorithm: {algorithm_luna(result)}\n\n'
        result_text += f'Lead time: {end:.2f} seconds'
        self.info_card.setText(
            f'Available card information: {self.setting["initial_digits"]}{result}{self.setting["last_digits"]}')
        self.result_label.setText(result_text)

    def update_pb_on_progress(self, i: int) -> None:
        """функция для обновляния прогресс pb

        Args:
            i (int): значение итерации
        """
        self.pbar.setValue(
            int((i + 1) / len(range(99999, 10000000)) * 100))

    def draw_graph(self) -> None:
        """функция для рисования графика
        """
        charting()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
