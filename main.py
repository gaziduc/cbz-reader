#!/usr/bin/python

import sys
from PyQt5.QtWidgets import *
from PyQt5 import *
from PyQt5.QtGui import *
from zipfile import ZipFile


class Window(QMainWindow):

    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle('CBZ Reader')
        self.resize(800, 600)

        actOpen = QAction(QIcon("icons/open.png"), "&Open", self)
        actOpen.triggered.connect(self.show_open_dialog)

        actExit = QAction(QIcon("icons/exit.png"), "&Quit", self)
        actExit.setShortcut("Ctrl+Q")
        actExit.triggered.connect(self.close)

        menuBar = self.menuBar()
        f = menuBar.addMenu("&File")
        f.addAction(actOpen)
        f.addSeparator()
        f.addAction(actExit)


        self.dropdown = QComboBox(self)
        self.dropdown.currentTextChanged.connect(self.load_and_show_image)

        self.label = QLabel(self)

        layout = QVBoxLayout()
        layout.addWidget(self.dropdown)
        layout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def show_open_dialog(self):
        filename, _ = QFileDialog.getOpenFileName(None, "Open a file...", "", "Comics (*.cbz)")

        if filename == None:
            return

        self.dropdown.clear();

        with ZipFile(filename, 'r') as zip_obj:

            zip_filenames = zip_obj.namelist()

            for zip_filename in zip_filenames:

                self.dropdown.addItem(zip_filename)
                zip_obj.extract(zip_filename, "tmp")

    def load_and_show_image(self):
        self.label.setPixmap(QPixmap("tmp/" + self.dropdown.currentText()))


def main():
    app = QApplication([])

    window = Window();
    window.show();

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
