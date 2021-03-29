from PySide2 import QtGui
from PySide2.QtWidgets import (QWidget, QDesktopWidget, QDialog, QPushButton,
                               QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel, QFrame, QTabWidget, QScrollArea)
from PySide2.QtCore import Slot, Qt, QTimer, QUrl
from PySide2.QtTextToSpeech import QTextToSpeech
from PySide2.QtGui import QFont
from PySide2.QtMultimedia import QSoundEffect
from blinkdetector import BlinkDetector
from symbolmanager import SymbolManager
from wordpredictor import WordPredictor

global TEXT_TIMER_DELAY, TEXT_SIZE, OVERLAY_TEXT_SIZE
TEXT_TIMER_DELAY = 1500
TEXT_SIZE = 14
OVERLAY_TEXT_SIZE = 14


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
        self.setWindowIcon(QtGui.QIcon('resources/icon.svg'))

        # Create buttons
        self.button_start = QPushButton("Start")
        self.button_start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_start.setStyleSheet("background-color: lightgreen")
        self.button_start.setFont(QFont("Helvetica", 14))
        self.button_start.clicked.connect(self.button_start_clicked)
        self.button_options = QPushButton("Options")
        self.button_options.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_options.setFont(QFont("Helvetica", 14))
        self.button_options.clicked.connect(self.button_options_clicked)
        self.button_help = QPushButton("Help")
        self.button_help.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.button_help.setFont(QFont("Helvetica", 14))
        self.button_help.clicked.connect(self.button_help_clicked)

        # Create layout and add buttons
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.button_start)
        self.layout.addWidget(self.button_options)
        self.layout.addWidget(self.button_help)
        self.setLayout(self.layout)

        self.dialog_window = None
        self.options_window = None
        self.help_window = None
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

    @Slot()
    def button_options_clicked(self):
        """
        Handler for the option button
        """
        self.options_window = OptionsWindow(self)

    @Slot()
    def button_help_clicked(self):
        """
        Handler for the help button
        """
        self.help_window = HelpWindow(self)

    def move_center(self):
        """
        Moves the window to the center of the screen
        """
        rect = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(center_point)
        self.move(rect.topLeft())


class OptionsWindow(QDialog):
    global TEXT_TIMER_DELAY, OVERLAY_TEXT_SIZE, TEXT_SIZE  # Pulls the timer delay and text size as global variables
    WINDOW_HEIGHT = 100      # Height of the window
    WINDOW_WIDTH = 400      # Width of the window

    def __init__(self, parent):
        super(OptionsWindow, self).__init__(parent)

        # Window configurations
        self.setWindowTitle("Options")
        self.setGeometry(0, 0, OptionsWindow.WINDOW_WIDTH, OptionsWindow.WINDOW_HEIGHT)
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2), (resolution.height() / 2) - (self.frameSize().height() / 2))

        # Create delay options
        self.delay_display = QLabel("Blink Controller Scroll Delay: " + str(TEXT_TIMER_DELAY/1000) + " s")
        self.delay_display.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.delay_display.setStyleSheet("font: 10pt")
        self.button_slower = QPushButton("+")
        self.button_slower.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_slower.setFixedSize(36, 36)
        self.button_slower.setFont(QFont("Helvetica", TEXT_SIZE))
        self.button_slower.clicked.connect(self.button_slower_clicked)
        self.button_faster = QPushButton("-")
        self.button_faster.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_faster.setFixedSize(36, 36)
        self.button_faster.setFont(QFont("Helvetica", TEXT_SIZE))
        self.button_faster.clicked.connect(self.button_faster_clicked)

        # Create text size options
        self.text_size_display = QLabel("Blink Controller Text Size: " + str(OVERLAY_TEXT_SIZE) + " pt")
        self.text_size_display.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.text_size_display.setStyleSheet("font: 10pt")
        self.button_larger = QPushButton("+")
        self.button_larger.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_larger.setFixedSize(36, 36)
        self.button_larger.setFont(QFont("Helvetica", TEXT_SIZE))
        self.button_larger.clicked.connect(self.button_larger_clicked)
        self.button_smaller = QPushButton("-")
        self.button_smaller.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.button_smaller.setFixedSize(36, 36)
        self.button_smaller.setFont(QFont("Helvetica", TEXT_SIZE))
        self.button_smaller.clicked.connect(self.button_smaller_clicked)

        # Create layouts to hold the labels
        self.delay_layout = QHBoxLayout()
        self.delay_layout.addWidget(self.button_slower)
        self.delay_layout.addWidget(self.button_faster)
        self.delay_layout.addWidget(self.delay_display)

        self.text_size_layout = QHBoxLayout()
        self.text_size_layout.addWidget(self.button_larger)
        self.text_size_layout.addWidget(self.button_smaller)
        self.text_size_layout.addWidget(self.text_size_display)

        self.v_layout = QVBoxLayout()
        self.v_layout.addLayout(self.delay_layout)
        self.v_layout.addLayout(self.text_size_layout)
        self.setLayout(self.v_layout)
        self.show()

    @Slot()
    def button_slower_clicked(self):
        """
        Handler for the faster scrolling button
        """
        global TEXT_TIMER_DELAY
        TEXT_TIMER_DELAY = TEXT_TIMER_DELAY + 100
        if TEXT_TIMER_DELAY > 3000:
            TEXT_TIMER_DELAY = 3000
        self.delay_display.setText("Blink Controller Scroll Delay: " + str(TEXT_TIMER_DELAY/1000) + " s")

    def button_faster_clicked(self):
        """
        Handler for the faster scrolling button
        """
        global TEXT_TIMER_DELAY
        TEXT_TIMER_DELAY = TEXT_TIMER_DELAY - 100
        if TEXT_TIMER_DELAY < 500:
            TEXT_TIMER_DELAY = 500
        self.delay_display.setText("Blink Controller Scroll Delay: " + str(TEXT_TIMER_DELAY/1000) + " s")

    def button_larger_clicked(self):
        """
        Handler for the larger text button
        """
        global OVERLAY_TEXT_SIZE
        OVERLAY_TEXT_SIZE += 1
        if OVERLAY_TEXT_SIZE > 15:
            OVERLAY_TEXT_SIZE = 15
        self.text_size_display.setText("Blink Controller Text Size: " + str(OVERLAY_TEXT_SIZE) + " pt")

    def button_smaller_clicked(self):
        """
        Handler for the smaller text button
        """
        global OVERLAY_TEXT_SIZE
        OVERLAY_TEXT_SIZE -= 1
        if OVERLAY_TEXT_SIZE < 8:
            OVERLAY_TEXT_SIZE = 8
        self.text_size_display.setText("Blink Controller Text Size: " + str(OVERLAY_TEXT_SIZE) + " pt")


class HelpWindow(QDialog):
    WINDOW_HEIGHT = 400      # Height of the window
    WINDOW_WIDTH = 400      # Width of the window

    def __init__(self, parent):
        super(HelpWindow, self).__init__(parent)

        # Window configurations
        self.setWindowTitle("Help")
        self.setGeometry(0, 0, HelpWindow.WINDOW_WIDTH, HelpWindow.WINDOW_HEIGHT)
        resolution = QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.frameSize().width() / 2), (resolution.height() / 2) - (self.frameSize().height() / 2))

        self.layout = QVBoxLayout(self)

        self.instructionsLabel = QLabel(self)
        self.instructionsLabel.setText("1. Adjust the camera to have a clear frontal view of your face.\n\n"
                                       "2. Click the start button to open the blink controller window.\n\n"
                                       "3. When a category scrolls into the selector, blink to open it.\n\n"
                                       "4. When a symbol scrolls into the selector, blink to input it.\n\n"
                                       "5. Continue steps 3 and 4 to form a sentence.\n\n"
                                       "6. Input the ENTER symbol to output the sentence as speech.\n\n"
                                       "7. When finished, click the stop button to close the blink controller.\n\n")
        self.instructionsLabel.setStyleSheet("font: 10pt")
        self.instructionsLabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.faqLabel = QLabel(self)
        self.faqLabel.setText("<b>Why is there a face not detected warning when I use the blink controller?</b><br>"
                              "The blink controller is having trouble detecting your face. "
                              "Ensure that your webcam has a clear frontal view of your face and your room"
                              " is well lit.<br><br>"
                              "<b>How do I input text?</b><br>"
                              "Select a category by blinking when it scrolls into the selector. "
                              "Next, select the word/phrase/letter/number you want to input by blinking "
                              "when it scrolls into the selector.<br><br>"
                              "<b>How do I output speech?</b><br>"
                              "After entering the text you want to say, select the FUNCTIONS category and select "
                              "the ENTER symbol. Your text will be converted to speech.<br><br>"
                              "<b>Why doesn't the application detect my blinks?</b><br>"
                              "Ensure that you make full blinks lasting around 1 second.")
        self.faqLabel.setStyleSheet("font: 10pt")
        self.faqLabel.setWordWrap(True)
        self.faqLabel.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.diagramPixmap = QtGui.QPixmap('resources/controller_diagram.png')
        self.diagramLabel = QLabel(self)
        self.diagramLabel.setPixmap(self.diagramPixmap)

        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tab3 = QWidget()
        self.tabs.setStyleSheet("font: 10pt")

        self.tabs.addTab(self.tab1, "Instructions For Use")
        self.tabs.addTab(self.tab2, "Frequently Asked Questions")
        self.tabs.addTab(self.tab3, "Diagram")

        self.tab1.layout = QVBoxLayout(self)
        self.tab1.layout.addWidget(self.instructionsLabel)
        self.tab1.setLayout(self.tab1.layout)

        self.tab2.layout = QVBoxLayout(self)
        self.tab2.layout.addWidget(self.faqLabel)
        self.tab2.setLayout(self.tab2.layout)

        self.tab3.layout = QVBoxLayout(self)
        self.tab3.layout.addWidget(self.diagramLabel)
        self.tab3.setLayout(self.tab3.layout)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.show()


class DialogWindow(QDialog):
    global TEXT_TIMER_DELAY, OVERLAY_TEXT_SIZE, TEXT_SIZE
    PAUSE_TIMER_DELAY = 100     # Defines the delay for the visual feedback when a blink is detected
    WINDOW_HEIGHT = 60      # Height of the dialog window
    WINDOW_WIDTH = 800      # Width of the dialog window

    def __init__(self, parent):
        super(DialogWindow, self).__init__(parent)

        # Window configurations
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(0, 0, DialogWindow.WINDOW_WIDTH, DialogWindow.WINDOW_HEIGHT)
        self.setContentsMargins(1, 1, 1, 1)

        self.symbol_manager = SymbolManager()

        self.tts = QTextToSpeech()

        self.setStyleSheet("border: 1px solid black")

        # Create labels
        self.output_label = QLabel("")
        self.output_label.setStyleSheet("background-color: white")
        self.output_label.setFont(QFont("Helvetica", OVERLAY_TEXT_SIZE + 2))
        self.output_label.setFrameStyle(QFrame.Panel | QFrame.Plain)

        self.suggestion_label1 = QLabel("")
        self.suggestion_label1.setStyleSheet("border-bottom: none; border-top: none; border-left: none")
        self.suggestion_label1.setAlignment(Qt.AlignCenter)
        self.suggestion_label1.setFont(QFont("Helvetica", OVERLAY_TEXT_SIZE))

        self.suggestion_label2 = QLabel("")
        self.suggestion_label2.setStyleSheet("border: none")
        self.suggestion_label2.setAlignment(Qt.AlignCenter)
        self.suggestion_label2.setFont(QFont("Helvetica", OVERLAY_TEXT_SIZE))

        self.suggestion_label3 = QLabel("")
        self.suggestion_label3.setStyleSheet("border-bottom: none; border-top: none; border-right: none")
        self.suggestion_label3.setAlignment(Qt.AlignCenter)
        self.suggestion_label3.setFont(QFont("Helvetica", OVERLAY_TEXT_SIZE))

        self.input_label1 = QLabel(self.symbol_manager.get_symbol_set(5)[0])
        self.input_label1.setStyleSheet("border: none")
        self.input_label1.setAlignment(Qt.AlignCenter)
        self.input_label1.setFont(QFont("Helvetica", OVERLAY_TEXT_SIZE + 2))
        self.input_label1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.input_label2 = QLabel(self.symbol_manager.get_symbol_set(5)[1])
        self.input_label2.setStyleSheet("border: none")
        self.input_label2.setAlignment(Qt.AlignCenter)
        self.input_label2.setFont(QFont("Helvetica", OVERLAY_TEXT_SIZE + 2))
        self.input_label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.input_label3 = QLabel(self.symbol_manager.get_symbol_set(5)[2])
        self.input_label3.setAlignment(Qt.AlignCenter)
        self.input_label3.setFont(QFont("Helvetica", OVERLAY_TEXT_SIZE + 2))
        self.input_label3.setFrameStyle(QFrame.Panel | QFrame.Plain)
        self.input_label3.setStyleSheet("QLabel { background-color: white; color: black; }")
        self.input_label3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.input_label4 = QLabel(self.symbol_manager.get_symbol_set(5)[3])
        self.input_label4.setStyleSheet("border: none")
        self.input_label4.setAlignment(Qt.AlignCenter)
        self.input_label4.setFont(QFont("Helvetica", OVERLAY_TEXT_SIZE + 2))
        self.input_label4.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.input_label5 = QLabel(self.symbol_manager.get_symbol_set(5)[4])
        self.input_label5.setStyleSheet("border: none")
        self.input_label5.setAlignment(Qt.AlignCenter)
        self.input_label5.setFont(QFont("Helvetica", OVERLAY_TEXT_SIZE + 2))
        self.input_label5.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.detected_label = QLabel("Face not detected. Adjust camera")
        self.detected_label.setAlignment(Qt.AlignCenter)
        self.detected_label.setFont(QFont("Helvetica", OVERLAY_TEXT_SIZE))
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

        self.word_predictor = WordPredictor()
        self.word_predictions = ["", "", ""]

        self.blink_timer = QTimer()
        self.blink_timer.timeout.connect(self.blink_detector.check_frame)

        self.pause_timer = QTimer()
        self.pause_timer.timeout.connect(self.handle_blink_end)

        self.blink_sound = QSoundEffect()
        self.blink_sound.setSource(QUrl.fromLocalFile("resources/sounds/ui_blink.wav"))

        self.move_top_middle()
        self.show()
        self.blink_timer.start()
        self.text_timer.start(TEXT_TIMER_DELAY)

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
        self.word_predictions = self.word_predictor.predict(self.symbol_manager.get_output_symbols())
        self.suggestion_label2.setText(self.word_predictions[0])
        self.suggestion_label1.setText(self.word_predictions[1])
        self.suggestion_label3.setText(self.word_predictions[2])
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
            self.suggestion_label2.setText(self.word_predictions[0])
            self.suggestion_label1.setText(self.word_predictions[1])
            self.suggestion_label3.setText(self.word_predictions[2])

            self.suggestion_label1.setStyleSheet("background-color: #F0F0F0;")
            self.suggestion_label1.setStyleSheet("border-bottom: none; border-top: none; border-left: none")
            self.suggestion_label2.setStyleSheet("border: none")
            self.suggestion_label3.setStyleSheet("border-bottom: none; border-top: none; border-right: none")
            self.suggestion_label2.show()
            self.suggestion_label3.show()
        else:
            self.suggestion_label1.setText("Face not detected. Adjust camera.")
            self.suggestion_label1.setStyleSheet("background-color: lightcoral; border: none")
            self.suggestion_label2.hide()
            self.suggestion_label3.hide()

    def keyPressEvent(self, event):
        """
        Space key mimicing a blink for debugging purposes
        """
        if event.key() == Qt.Key_Space:
            self.handle_blink_start()
        event.accept()


class ScrollLabel(QScrollArea):

    def __init__(self, *args, **kwargs):
        QScrollArea.__init__(self, *args, **kwargs)

        self.setWidgetResizable(True)
        content = QWidget(self)
        self.setWidget(content)
        lay = QVBoxLayout(content)
        self.label = QLabel(content)
        self.label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.label.setWordWrap(True)
        lay.addWidget(self.label)

    def setText(self, text):
        self.label.setText(text)

