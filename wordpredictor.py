import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.layers import Embedding, Dense, LSTM, Dropout
from tensorflow.keras.models import Sequential
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import load_model


class WordPredictor:

    def __init__(self):
        self.model = load_model('resources/char_model.h5')
        self.tokenizer = Tokenizer(char_level=True)
        self.tokenizer.fit_on_texts("abcdefghijklmnopqrstuvwxyz' ")
        self.int_to_char = dict((i + 1, c) for i, c in enumerate(self.tokenizer.word_index))

    @staticmethod
    def train_model():
        X_data = []
        y_data = []
        chars = "abcdefghijklmnopqrstuvwxyz' "
        with open("words.txt", "r") as file:
            words = file.readlines()
            for word in words:
                word = word.rstrip()
                word = word + " "
                X_word = ""
                for j in range(len(word) - 1):
                    X_word += word[j]
                    X_data.append(X_word)
                    y_data.append(word[j+1])

        X_data = np.array(X_data)
        y_data = np.array(y_data)

        tokenizer = Tokenizer(char_level=True)
        tokenizer.fit_on_texts(chars)

        X_data = tokenizer.texts_to_sequences(X_data)
        y_data = tokenizer.texts_to_sequences(y_data)
        y_data = to_categorical(y_data)

        X_data = pad_sequences(X_data, maxlen=30)

        X_data = np.array(X_data)
        y_data = np.array(y_data)

        model = Sequential()
        model.add(Embedding(len(chars), 50, input_length=30))
        model.add(LSTM(200, return_sequences=True))
        model.add(Dropout(0.2))
        model.add(LSTM(200))
        model.add(Dropout(0.2))
        model.add(Dense(len(y_data[0]), activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam')
        model.fit(X_data, y_data, epochs=50, batch_size=128, validation_split=0.1)
        model.save('resources/char_model.h5')

    def predict_word(self, input_text):
        text = np.array([input_text])
        text = self.tokenizer.texts_to_sequences(text)
        text = pad_sequences(text, maxlen=30)
        ch = np.argmax(self.model.predict(np.array(text)))
        ch = self.int_to_char[int(ch)]
        if ch == " " or len(input_text) > 25:
            return input_text
        else:
            return self.predict_word(input_text + ch)

    def predict_three_words(self, input_text):
        words = ["", "", ""]
        text = np.array([input_text])
        text = self.tokenizer.texts_to_sequences(text)
        text = pad_sequences(text, maxlen=30)
        prob = self.model.predict(np.array(text)).flatten()
        ch = np.argsort(-prob)
        prob = [prob[ch[0]], prob[ch[1]], prob[ch[2]]]
        ch = [self.int_to_char[ch[0]], self.int_to_char[ch[1]], self.int_to_char[ch[2]]]
        for i in range(3):
            if prob[i] < 0.1 or len(input_text) > 25:
                words[i] = ""
            elif ch[i] == " ":
                words[i] = input_text
            else:
                words[i] = self.predict_word(input_text + ch[i])
        return np.array(words)

    def predict(self, input_text):
        text = ""
        in_text = input_text.lower()
        for i in range(len(in_text)):
            if in_text[i] == " ":
                text = ""
            else:
                text += in_text[i]
        if text == "":
            return np.array(["", "", ""])
        else:
            return self.predict_three_words(text)

