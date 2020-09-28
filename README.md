<h1 align="center"> Blink Controlled Speech Synthesizer </h1>

<p align="center">
<img alt="GitHub top language" src="https://img.shields.io/github/languages/top/jakeegan/blink-controlled-speech-synthesizer">
<img alt="GitHub issues" src="https://img.shields.io/github/issues/jakeegan/blink-controlled-speech-synthesizer">
<img alt="GitHub" src="https://img.shields.io/github/license/jakeegan/Blink-Controlled-Speech-Synthesizer">
</p>

## Description
An application designed to synthesize speech solely through the control of blink gestures to enable communication for people suffering from paralysis.

## Installation
Requires python 3.7 and the libraries in requirements.txt

Clone this repo:
```
git clone https://github.com/jakeegan/Blink-Controlled-Speech-Synthesizer
cd Blink-Controlled-Speech-Synthesizer
```
Install dependencies:
```
pip install -r requirements.txt
```
Run the program:
```
python __main__.py 
```

## Folder structure
```
.
│   .gitignore
│   LICENSE
│   README.md
│   requirements.txt ========> python dependencies
|   main.py
|   gui.py
|   blinkdetector.py
|   textmanager.py
│
├───resources
│   │   blink_model.pk1 ========> blink detector svm model
│   │   shape_predictor_68_face_landmarks.dat ========> landmark detector model
│   └───datasets
|   |   |   ear_output_eyeblink8.txt ========> calculated eye aspect ratios for the eyeblink8 dataset
|   |   |   labels_eyeblink8.txt ========> ground truth values for the eyeblink8 dataset
│   └───sounds
|   |   |   ui_blink.wav ========> sound for when a blink is detected
```

## Architecture
