from PySide2.QtWidgets import (QWidget, QDesktopWidget, QDialog, QPushButton,
                               QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel, QFrame)
from PySide2.QtCore import Slot, Qt, QTimer, QUrl, QEvent
from PySide2.QtTextToSpeech import QTextToSpeech
from PySide2.QtGui import QFont
from PySide2.QtMultimedia import QSoundEffect
from blinkdetector import BlinkDetector
from symbolmanager import SymbolManager


class MainWindow(QWidget):
    """
    Contains the MainWindow and DialogWindow classes, created using Qt for Python/PySide2.
    The classes implement all the GUI for the program.
    """
    WINDOW_HEIGHT = 60  # Height of the main window
    WINDOW_WIDTH = 260  # Width of the main window

    def __init__(self):
        super().__init__()

        self.input_enabled = False  # boolean representing whether the program is accepting blink input

        # Window configurations
        self.setWindowTitle("Blink2Talk")
        self.setGeometry(0, 0, MainWindow.WINDOW_WIDTH, MainWindow.WINDOW_HEIGHT)
        self.move_center()

        # Create buttons
        self.button_start = QPushButton("Start")
        self.button_start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_start.setStyleSheet("background-color: lightgreen")
        self.button_start.setFont(QFont("Helvetica", 14))
        self.button_start.clicked.connect(self.button_start_clicked)
        self.button_options = QPushButton("Options")
        self.button_options.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_options.setFont(QFont("Helvetica", 14))
        self.button_help = QPushButton("Help")
        self.button_help.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_help.setFont(QFont("Helvetica", 14))

        # Create layout and add buttons
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.button_start)
        self.layout.addWidget(self.button_options)
        self.layout.addWidget(self.button_help)
        self.setLayout(self.layout)

        self.dialog_window = None
        self.show()

    @Slot()
    def button_start_clicked(self):
        """
        Handler for the start button
        """
        if self.input_enabled:
            self.input_enabled = False
            self.button_start.setText("Start")
            self.button_start.setStyleSheet("background-color: lightgreen")
            self.dialog_window.close()
            self.dialog_window.destroy()
            self.dialog_window.blink_detector = None
        else:
            self.input_enabled = True
            self.button_start.setText("Stop")
            self.button_start.setStyleSheet("background-color: lightcoral")
            self.dialog_window = DialogWindow(self)

    def move_center(self):
        """
        Moves the window to the center of the screen
        """
        rect = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(center_point)
        self.move(rect.topLeft())


class DialogWindow(QDialog):
    TEXT_TIMER_DELAY = 1500     # Defines the speed of the text scrolling in miliseconds
    PAUSE_TIMER_DELAY = 100     # Defines the delay for the visual feedback when a blink is detected
    WINDOW_HEIGHT = 60      # Height of the dialog window
    WINDOW_WIDTH = 600      # Width of the dialog window

    def __init__(self, parent):
        super(DialogWindow, self).__init__(parent)

        # Window configurations
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, DialogWindow.WINDOW_WIDTH, DialogWindow.WINDOW_HEIGHT)

        self.symbol_manager = SymbolManager()

        self.tts = QTextToSpeech()

        # Create labels
        self.output_label = QLabel("")
        self.output_label.setStyleSheet("background-color: white")
        self.output_label.setFont(QFont("Helvetica", 16))
        self.output_label.setFrameStyle(QFrame.Panel | QFrame.Plain)

        self.suggestion_label1 = QLabel("suggestion1")
        self.suggestion_label1.setAlignment(Qt.AlignCenter)
        self.suggestion_label1.setFont(QFont("Helvetica", 14))

        self.suggestion_label2 = QLabel("suggestion2")
        self.suggestion_label2.setAlignment(Qt.AlignCenter)
        self.suggestion_label2.setFont(QFont("Helvetica", 14))

        self.suggestion_label3 = QLabel("suggestion3")
        self.suggestion_label3.setAlignment(Qt.AlignCenter)
        self.suggestion_label3.setFont(QFont("Helvetica", 14))

        self.input_label1 = QLabel(self.symbol_manager.get_symbol_set(5)[0])
        self.input_label1.setAlignment(Qt.AlignCenter)
        self.input_label1.setFont(QFont("Helvetica", 16))
        self.input_label1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.input_label2 = QLabel(self.symbol_manager.get_symbol_set(5)[1])
        self.input_label2.setAlignment(Qt.AlignCenter)
        self.input_label2.setFont(QFont("Helvetica", 16))
        self.input_label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.input_label3 = QLabel(self.symbol_manager.get_symbol_set(5)[2])
        self.input_label3.setAlignment(Qt.AlignCenter)
        self.input_label3.setFont(QFont("Helvetica", 16))
        self.input_label3.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.input_label3.setStyleSheet("QLabel { background-color: white; color: black; }")
        self.input_label3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.input_label4 = QLabel(self.symbol_manager.get_symbol_set(5)[3])
        self.input_label4.setAlignment(Qt.AlignCenter)
        self.input_label4.setFont(QFont("Helvetica", 16))
        self.input_label4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.input_label5 = QLabel(self.symbol_manager.get_symbol_set(5)[4])
        self.input_label5.setAlignment(Qt.AlignCenter)
        self.input_label5.setFont(QFont("Helvetica", 16))
        self.input_label5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.detected_label = QLabel("Face not detected. Adjust camera")
        self.detected_label.setAlignment(Qt.AlignCenter)
        self.detected_label.setFont(QFont("Helvetica", 14))
        self.detected_label.hide()

        # Create layouts to hold the labels
        self.suggestion_labels = QHBoxLayout()
        self.suggestion_labels.addWidget(self.suggestion_label1)
        self.suggestion_labels.addWidget(self.suggestion_label2)
        self.suggestion_labels.addWidget(self.suggestion_label3)

        self.input_labels = QHBoxLayout()
        self.input_labels.addWidget(self.input_label1)
        self.input_labels.addWidget(self.input_label2)
        self.input_labels.addWidget(self.input_label3)
        self.input_labels.addWidget(self.input_label4)
        self.input_labels.addWidget(self.input_label5)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.output_label)
        self.v_layout.addLayout(self.suggestion_labels)
        self.v_layout.addLayout(self.input_labels)
        self.v_layout.addWidget(self.detected_label)
        self.setLayout(self.v_layout)

        # Initialize timers
        self.text_timer = QTimer()
        self.text_timer.timeout.connect(self.symbol_scroll)

        self.blink_detector = BlinkDetector(0, False)
        self.blink_detector.face_detected.connect(self.update_detected_label)
        self.blink_detector.blink_detected.connect(self.handle_blink_start)

        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.blink_detector.check_frame)

        self.pause_timer = QTimer()
        self.pause_timer.timeout.connect(self.handle_blink_end)

        self.blink_sound = QSoundEffect()
        self.blink_sound.setSource(QUrl.fromLocalFile("resources/sounds/ui_blink.wav"))

        self.move_top_middle()
        self.show()
        self.blink_timer.start()
        self.text_timer.start(DialogWindow.TEXT_TIMER_DELAY)

    @Slot()
    def symbol_scroll(self):
        """
        Scroll the symbols and update the GUI
        """
        self.symbol_manager.scroll_symbols()
        self.input_label1.setText(self.symbol_manager.get_symbol_set(5)[0])
        self.input_label2.setText(self.symbol_manager.get_symbol_set(5)[1])
        self.input_label3.setText(self.symbol_manager.get_symbol_set(5)[2])
        self.input_label4.setText(self.symbol_manager.get_symbol_set(5)[3])
        self.input_label5.setText(self.symbol_manager.get_symbol_set(5)[4])

    @Slot()
    def handle_blink_start(self):
        """
        Implements all the functionality needed after a blink is detected
        """
        # Pause operation
        self.blink_timer.stop()
        self.text_timer.stop()
        # Give auditory and visual feedback
        self.input_label3.setStyleSheet("background-color: lightgreen; color: black;")
        self.blink_sound.play()
        # Wait 0.1 sec
        self.pause_timer.start(DialogWindow.PAUSE_TIMER_DELAY)

    @Slot()
    def handle_blink_end(self):
        """
        Implements all the functionality needed after a blink is detected and a delay
        """
        # Handle the entered symbol
        self.symbol_manager.add_current_symbol()
        self.output_label.setText(self.symbol_manager.get_output_symbols())
        self.input_label1.setText(self.symbol_manager.get_symbol_set(5)[0])
        self.input_label2.setText(self.symbol_manager.get_symbol_set(5)[1])
        self.input_label3.setText(self.symbol_manager.get_symbol_set(5)[2])
        self.input_label4.setText(self.symbol_manager.get_symbol_set(5)[3])
        self.input_label5.setText(self.symbol_manager.get_symbol_set(5)[4])
        self.input_label3.setStyleSheet("background-color: white; color: black;")
        # Commence operation
        self.text_timer.start(DialogWindow.TEXT_TIMER_DELAY)
        self.blink_timer.start()
        self.pause_timer.stop()

    def move_top_middle(self):
        """
        Moves the overlay to the top middle of the screen
        """
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2), 0)

    @Slot(bool)
    def update_detected_label(self, face_detected):
        """
        Updates the GUI to tell the user if a face is not detected by the blink detector
        """
        if face_detected:
            self.suggestion_label1.setText("suggestion1")
            self.suggestion_label1.setStyleSheet("background-color: #F0F0F0;")
            self.suggestion_label2.show()
            self.suggestion_label3.show()
        else:
            self.suggestion_label1.setText("Face not detected. Adjust camera.")
            self.suggestion_label1.setStyleSheet("background-color: lightcoral;")
            self.suggestion_label2.hide()
            self.suggestion_label3.hide()

    def keyPressEvent(self, event):
        """
        Space key mimicing a blink for debugging purposes
        """
        if event.key() == Qt.Key_Space:
            self.handle_blink_start()
        event.accept()
