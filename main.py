# ----------------------------------------------------------------------------------------------------------------------
# Contains the main function which creates a QApplication.
# ----------------------------------------------------------------------------------------------------------------------
# pyinstaller main.py -F -w -i resources/icon.ico
import sys
from PySide2.QtWidgets import (QApplication)
from gui import MainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
