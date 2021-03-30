from fast_autocomplete import autocomplete_factory
import numpy as np
import json


class WordPredictor:

    def __init__(self):
        self.autoComplete = autocomplete_factory(
            content_files={'words': {'filepath': 'resources/words.json', 'compress': True}})

    @staticmethod
    def make_json():
        with open("resources/datasets/words10k.txt", "r") as file:
            words = file.readlines()
            for i in range(len(words)):
                words[i] = words[i].rstrip().lower()
        words = {words[i]: [{}, words[i], 10000 - int(i/2)] for i in range(0, len(words), 2)}
        with open('resources/words.json', 'w') as outfile:
            json.dump(words, outfile)

    def predict(self, text):
        text = text.lower()
        if text == "" or text == " " or text[-1] == " ":
            return np.array(["", "", ""])
        else:
            text = text.split()
            text = text[len(text)-1]
            pred = self.autoComplete.search(word=text, max_cost=3, size=3)
            while len(pred) < 3:
                pred.append([""])
            return np.array(pred).flatten()


#wordPredictor = WordPredictor()
#wordPredictor.make_json()
#print(wordPredictor.predict(""))
#print(wordPredictor.predict(" "))
#print(wordPredictor.predict("the "))
#print(wordPredictor.predict("the b"))
#print(wordPredictor.predict("b"))
#print(wordPredictor.predict("lolrandomstring"))
#print(wordPredictor.predict("hi how "))
#print(wordPredictor.predict("hel"))