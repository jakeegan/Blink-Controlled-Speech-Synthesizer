# ----------------------------------------------------------------------------------------------------------------------
# Contains the MainWindow and DialogWindow classes, created using Qt for Python, or PySide2. The classes implement
# all the GUI for the program.
# ----------------------------------------------------------------------------------------------------------------------
from PySide2.QtWidgets import (QLineEdit, QWidget, QDesktopWidget, QDialog, QPushButton,
                               QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel)
from PySide2.QtCore import Slot, Qt, QTimer, QUrl
from PySide2.QtTextToSpeech import QTextToSpeech
from PySide2.QtGui import QFont
from PySide2.QtMultimedia import QSoundEffect
from blinkdetector import BlinkDetector
from textmanager import TextManager


class MainWindow(QWidget):
    WINDOW_HEIGHT = 60
    WINDOW_WIDTH = 260

    def __init__(self):
        super().__init__()

        self.input_enabled = False

        self.setWindowTitle("Capstone")
        self.setGeometry(0, 0, MainWindow.WINDOW_WIDTH, MainWindow.WINDOW_HEIGHT)
        self.move_center()

        self.button_start = QPushButton("Start")
        self.button_start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_start.setStyleSheet("background-color: green")
        self.button_start.setFont(QFont("Helvetica", 14))
        self.button_start.clicked.connect(self.button_start_clicked)
        self.button_options = QPushButton("Options")
        self.button_options.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_options.setFont(QFont("Helvetica", 14))
        self.button_help = QPushButton("Help")
        self.button_help.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_help.setFont(QFont("Helvetica", 14))

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.button_start)
        self.layout.addWidget(self.button_options)
        self.layout.addWidget(self.button_help)
        self.setLayout(self.layout)

        self.dialog_window = None

        self.show()

    @Slot()
    def button_start_clicked(self):
        if self.input_enabled:
            self.input_enabled = False
            self.button_start.setText("Start")
            self.button_start.setStyleSheet("background-color: green")
            self.dialog_window.close()
        else:
            self.input_enabled = True
            self.button_start.setText("Stop")
            self.button_start.setStyleSheet("background-color: red")
            self.dialog_window = DialogWindow(self)

    def move_center(self):
        rect = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(center_point)
        self.move(rect.topLeft())


class DialogWindow(QDialog):
    TEXT_TIMER_DELAY = 1500
    WINDOW_HEIGHT = 60
    WINDOW_WIDTH = 400

    def __init__(self, parent):
        super(DialogWindow, self).__init__(parent)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, DialogWindow.WINDOW_WIDTH, DialogWindow.WINDOW_HEIGHT)

        self.text_manager = TextManager()

        self.tts = QTextToSpeech()

        self.output_label = QLineEdit("")
        self.output_label.setStyleSheet("background-color: white")
        self.output_label.setFont(QFont("Helvetica", 12))

        self.suggestions_label1 = QLabel("suggestion1")
        self.suggestions_label1.setAlignment(Qt.AlignCenter)
        self.suggestions_label1.setFont(QFont("Helvetica", 11))

        self.suggestions_label2 = QLabel("|")
        self.suggestions_label2.setAlignment(Qt.AlignCenter)
        self.suggestions_label2.setFont(QFont("Helvetica", 11))

        self.suggestions_label3 = QLabel("suggestion2")
        self.suggestions_label3.setAlignment(Qt.AlignCenter)
        self.suggestions_label3.setFont(QFont("Helvetica", 11))

        self.suggestions_label4 = QLabel("|")
        self.suggestions_label4.setAlignment(Qt.AlignCenter)
        self.suggestions_label4.setFont(QFont("Helvetica", 11))

        self.suggestions_label5 = QLabel("suggestion3")
        self.suggestions_label5.setAlignment(Qt.AlignCenter)
        self.suggestions_label5.setFont(QFont("Helvetica", 11))

        self.input_label = QLineEdit(self.text_manager.get_symbol_set())
        self.input_label.setStyleSheet("background-color: white")
        self.input_label.setFont(QFont("Helvetica", 12))
        self.input_label.setCursorPosition(0)
        self.input_label.setSelection(1, len(self.text_manager.get_current_symbol())+2)

        self.detected_label = QLabel("Face not detected. Adjust camera")
        self.detected_label.setAlignment(Qt.AlignCenter)
        self.detected_label.setFont(QFont("Helvetica", 11))
        self.detected_label.hide()

        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.suggestions_label1)
        self.h_layout.addWidget(self.suggestions_label2)
        self.h_layout.addWidget(self.suggestions_label3)
        self.h_layout.addWidget(self.suggestions_label4)
        self.h_layout.addWidget(self.suggestions_label5)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.output_label)
        self.v_layout.addLayout(self.h_layout)
        self.v_layout.addWidget(self.input_label)
        self.v_layout.addWidget(self.detected_label)
        self.setLayout(self.v_layout)

        self.text_timer = QTimer()
        self.text_timer.timeout.connect(self.symbol_scroll)

        self.blink_detector = BlinkDetector(0, False)
        self.blink_detector.face_detected.connect(self.update_detected_label)
        self.blink_detector.blink_detected.connect(self.handle_blink)

        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.blink_detector.check_frame)

        self.blink_sound = QSoundEffect()
        self.blink_sound.setSource(QUrl.fromLocalFile("resources/sounds/ui_blink.wav"))

        self.move_top_middle()
        self.show()
        self.blink_timer.start()
        self.text_timer.start(DialogWindow.TEXT_TIMER_DELAY)

    @Slot()
    def symbol_scroll(self):
        self.text_manager.scroll_symbols()
        self.input_label.setText(self.text_manager.get_symbol_set())
        self.input_label.setCursorPosition(0)
        self.input_label.setSelection(1, len(self.text_manager.get_current_symbol())+2)

    @Slot()
    def handle_blink(self):
        self.blink_sound.play()
        self.text_manager.add_current_symbol()
        self.output_label.setText(self.text_manager.get_output_symbols())
        self.input_label.setText(self.text_manager.get_symbol_set())
        self.input_label.setCursorPosition(0)
        self.input_label.setSelection(1, len(self.text_manager.get_current_symbol())+2)
        self.text_timer.start(DialogWindow.TEXT_TIMER_DELAY)

    def move_top_middle(self):
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2), 0)

    @Slot(bool)
    def update_detected_label(self, face_detected):
        if face_detected:
            self.suggestions_label1.setText("suggestion1")
            self.suggestions_label2.show()
            self.suggestions_label3.show()
            self.suggestions_label4.show()
            self.suggestions_label5.show()
        else:
            self.suggestions_label1.setText("Face not detected. Adjust camera.")
            self.suggestions_label2.hide()
            self.suggestions_label3.hide()
            self.suggestions_label4.hide()
            self.suggestions_label5.hide()
