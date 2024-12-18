<p align="center"><img src="/resources/icon.png"></p>
<h1 align="center"> Blink2Talk </h1>

## Description
An application designed to synthesize speech solely through the control of blink gestures to enable communication for people suffering from paralysis.

## State Diagram
A state diagram depicting the behaviour of the blink controller.

![State Diagram](resources/state_diagram.png)

## Input Table
The following table shows the possible symbols that the user can input.

| FUNCTIONS | WORDS     | LETTERS(a-m) | LETTERS(n-z) | NUMBERS |
|-----------|-----------|--------------|--------------|---------|
| ENTER     | hello     | a            | n            | 0       |
| ERASE     | bye       | b            | o            | 1       |
| SPACE     | yes       | c            | p            | 2       |
| TAB       | no        | d            | q            | 3       |
| ALT       | thank you | e            | r            | 4       |
| CTRL      | sorry     | f            | s            | 5       |
| SHIFT     | good      | g            | t            | 6       |
| ESC       | bad       | h            | u            | 7       |
| DELETE    | hungry    | i            | v            | 8       |
|           | thirsty   | j            | w            | 9       |
|           | happy     | k            | x            |         |
|           | sad       | l            | y            |         |
|           | help      | m            | z            |         |

## Installation
Requires python 3.7 and the libraries in requirements.txt

### With PyCharm and virtual environment
Clone this repo:
```
git clone https://github.com/jakeegan/Blink-Controlled-Speech-Synthesizer
```
1. Open PyCharm and start a new project
2. Set project location to where you cloned the repo
3. Select "New environment using" and choose "Virtualenv" from the drop down menu
4. Click create
5. Double click "__main__.py"
6. It will say "Package requirements are not satisfied". Click install requirements
7. Right click "__main__.py" and click run

### Without PyCharm
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
