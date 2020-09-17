# ----------------------------------------------------------------------------------------------------------------------
# The TextManager class contains all the functions needed to handle the text input and output for the program.
# ----------------------------------------------------------------------------------------------------------------------
from PySide2.QtTextToSpeech import QTextToSpeech


class TextManager:
    SYMBOLS = [["SWAP", "ENTER", "ERASE", "SPACE", "hello ", "bye ", "yes ", "no ", "thank you ",
                "good ", "bad ", "hungry ", "thirsty "],
               ["SWAP", "ENTER", "ERASE", "SPACE", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
                "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"],
               ["SWAP", "ENTER", "ERASE", "SPACE", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"],
               ["SWAP", "ENTER", "ERASE", "SPACE", "TAB", "ALT", "CTRL", "SHIFT", "ESC", "DELETE"]]

    def __init__(self):
        self.symbol_set = 0
        self.current_symbol = 0
        self.symbol_output = []
        self.tts = QTextToSpeech()

    # Called every x seconds by the main program to scroll through symbols
    def scroll_symbols(self):
        self.current_symbol += 1
        if self.current_symbol == len(TextManager.SYMBOLS[self.symbol_set]):
            self.current_symbol = 0

    # Returns the list of output symbols
    def get_output_symbols(self):
        temp = ""
        for i in range(len(self.symbol_output)):
            temp += self.symbol_output[i]
        return temp

    # Returns the list of symbols from the current set, starting at the current symbol
    def get_symbol_set(self):
        temp = ""
        for i in range(self.current_symbol, len(TextManager.SYMBOLS[self.symbol_set])):
            temp += "[ "
            temp += TextManager.SYMBOLS[self.symbol_set][i]
            temp += " ]"
        for i in range(0, self.current_symbol):
            temp += "[ "
            temp += TextManager.SYMBOLS[self.symbol_set][i]
            temp += " ]"
        return temp

    # Add current symbol to symbol output, used when a blink is detected
    def add_current_symbol(self):
        symbol = TextManager.SYMBOLS[self.symbol_set][self.current_symbol]
        if symbol == "SWAP":
            self.swap_symbol_set()
        elif symbol == "ENTER":
            self.tts.say(self.get_output_symbols())
            self.symbol_output = []
        elif symbol == "ERASE":
            if len(self.symbol_output) > 0:
                self.symbol_output.pop()
        elif symbol == "SPACE":
            self.symbol_output.append(" ")
        else:
            self.symbol_output.append(symbol)
        self.current_symbol = 0

    # Returns the last symbol that was saved to the output symbol list
    def get_last_symbol(self):
        return self.symbol_output[len(self.symbol_output) - 1]

    # Returns the first symbol in the list
    # Is used when the user blinks
    def get_current_symbol(self):
        return TextManager.SYMBOLS[self.symbol_set][self.current_symbol]

    # Swaps to the next symbol set
    def swap_symbol_set(self):
        self.symbol_set += 1
        if self.symbol_set == len(TextManager.SYMBOLS):
            self.symbol_set = 0
