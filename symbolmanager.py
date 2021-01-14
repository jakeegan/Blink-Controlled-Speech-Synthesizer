from PySide2.QtTextToSpeech import QTextToSpeech
from pynput.keyboard import Key, Controller


class SymbolManager:
    """
    The SymbolManager class contains all the functions needed to handle the symbol input and output for the program.
    """
    SYMBOLS = [["", "", "FUNCTIONS", "WORDS", "LETTERS(a-m)", "LETTERS(n-z)", "NUMBERS", "", ""],
               ["", "", "ENTER", "ERASE", "SPACE", "TAB", "ALT", "CTRL", "SHIFT", "ESC", "DELETE", "", ""],
               ["", "", "hello ", "bye ", "yes ", "no ", "thank you ", "sorry ", "good ", "bad ", "hungry ", "thirsty ", "happy ", "sad ", "help ", "", ""],
               ["", "", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "", ""],
               ["", "", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "", ""],
               ["", "", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "", ""]]

    def __init__(self):
        self.current_set = 0     # The index for a set in the SYMBOLS array
        self.current_symbol = 0     # The index for the current symbol in SYMBOLS array
        self.symbol_output = []     # Contains a list of symbols for output
        self.tts = QTextToSpeech()      # Text to speech object
        self.key_controller = Controller()      # Keyboard output object
        self.mode = "talk"  # Two modes: talk or keyboard

    def scroll_symbols(self):
        """
        Sets current symbol to the next one in the set. Called every x seconds by the program.
        """
        self.current_symbol += 1
        if self.current_symbol == len(SymbolManager.SYMBOLS[self.current_set]):
            self.current_symbol = 0

    def get_output_symbols(self):
        """
        Returns the output of symbols as a string
        """
        out = ""
        for i in range(len(self.symbol_output)):
            out += self.symbol_output[i]
        return out

    def get_symbol_set(self, length):
        """
        Returns a list of specified length containing symbols from the current set, starting at the current symbol
        """
        out = []
        count = 0
        if self.current_symbol - length//2 < 0:
            i = len(SymbolManager.SYMBOLS[self.current_set]) + self.current_symbol - length//2
        else:
            i = self.current_symbol - length//2

        while count < length:
            out.append(SymbolManager.SYMBOLS[self.current_set][i])
            i += 1
            if i >= len(SymbolManager.SYMBOLS[self.current_set]):
                i = 0
            count += 1
        return out

    def add_current_symbol(self):
        """
        Handles current symbol when a blink is detected.
        """
        symbol = SymbolManager.SYMBOLS[self.current_set][self.current_symbol]
        if symbol == "FUNCTIONS":
            self.current_set = 1
            self.current_symbol = 0
        elif symbol == "WORDS":
            self.current_set = 2
            self.current_symbol = 0
        elif symbol == "LETTERS(a-m)":
            self.current_set = 3
            self.current_symbol = 0
        elif symbol == "LETTERS(n-z)":
            self.current_set = 4
            self.current_symbol = 0
        elif symbol == "NUMBERS":
            self.current_set = 5
            self.current_symbol = 0
        elif symbol == "ENTER":
            self.tts.say(self.get_output_symbols())
            self.symbol_output = []
            self.current_set = 0
            self.current_symbol = 0
        elif symbol == "ERASE":
            if len(self.symbol_output) > 0:
                self.symbol_output.pop()
            self.current_set = 0
            self.current_symbol = 0
        elif symbol == "SPACE":
            self.symbol_output.append(" ")
            self.current_set = 0
            self.current_symbol = 0
        elif symbol == "TAB":
            self.key_controller.press(Key.tab)
            self.key_controller.release(Key.tab)
            self.current_set = 0
            self.current_symbol = 0
        elif symbol == "ALT":
            self.key_controller.press(Key.alt)
            self.key_controller.release(Key.alt)
            self.current_set = 0
            self.current_symbol = 0
        elif symbol == "CTRL":
            self.key_controller.press(Key.ctrl)
            self.key_controller.release(Key.ctrl)
            self.current_set = 0
            self.current_symbol = 0
        elif symbol == "SHIFT":
            self.key_controller.press(Key.shift)
            self.key_controller.release(Key.shift)
            self.current_set = 0
            self.current_symbol = 0
        elif symbol == "ESC":
            self.key_controller.press(Key.esc)
            self.key_controller.release(Key.esc)
            self.current_set = 0
            self.current_symbol = 0
        elif symbol == "DELETE":
            self.key_controller.press(Key.delete)
            self.key_controller.release(Key.delete)
            self.current_set = 0
            self.current_symbol = 0
        elif symbol == "":
            pass
        else:
            self.symbol_output.append(symbol)
            self.current_set = 0
            self.current_symbol = 0
