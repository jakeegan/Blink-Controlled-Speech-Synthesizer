import time
import dlib
import cv2
import pickle
from PySide2.QtCore import QObject, Signal, Slot
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix


class BlinkDetector(QObject):
    """
    The BlinkDetector class fetches frames from the webcam, detects a face, applies landmark detection on the face,
    calculates the eye aspect ratio of the eye, creates a 13-dimensional feature vector with the eye aspect ratio
    values, then uses an svm to classify between non-blink and blink states. When a blink is detected, the main program
    is notified through a Qt signal. The class also contains functions to obtain eye aspect ratio values from a
    video file and train an SVM. The SVM is trained on the eyeblink8 dataset.
    """
    LEFT_EYE_OFFSET = 36    # Starting position for the left eye in landmark array
    RIGHT_EYE_OFFSET = 42   # Starting position for the right eye in landmark array
    SKIP_FRAMES = 2     # Number of frames to skip for face detector
    DOWNSIZE_RATIO = 2  # The ratio to downsize video frames
    EAR_THRESHOLD = 0.25    # Threshold for eye aspect ratio
    EAR_FEATURE_SIZE = 13   # Size of eye aspect ratio array
    EAR_FEATURE_SIZE_HALF = 6   # Half size of eye aspect ratio array

    face_detected = Signal(bool)
    blink_detected = Signal()

    def __init__(self, file_path, draw_mode):
        super(BlinkDetector, self).__init__()
        self.draw_mode = draw_mode  # Enable/disable drawing of landmarks
        self.ear_feature = []   # Eye aspect ratio feature array
        self.faces = []     # Array to hold detected faces
        self.frame_count = 0    # Video frame counter
        self.frames_per_sec = 0     # Frames per second processed by blink detector
        self.last_blink_frame = 0   # Last frame that a blink was detected
        with open('resources/blink_model.pk1', 'rb') as f:
            self.blink_svm = pickle.load(f)
        self.face_detector = dlib.get_frontal_face_detector()
        self.landmark_detector = dlib.shape_predictor("resources/shape_predictor_68_face_landmarks.dat")
        self.cap = cv2.VideoCapture(file_path)  # filePath = 0 for front cam
        self.start_time = time.time()

    @staticmethod
    def scale_dlib_rect(rect, scale):
        """
        Scales a dlib rectangle object by the specified amount
        :param rect:<rectangle> The object to be scaled
        :param scale:<float> The scale factor
        """
        left = rect.left() * scale
        top = rect.top() * scale
        right = rect.right() * scale
        bottom = rect.bottom() * scale
        return dlib.rectangle(left, top, right, bottom)

    @staticmethod
    def calc_ear(landmarks, offset):
        """
        Calculates eye aspect ratio with landmark positions
        :param landmarks:<array> Array holding facial landmarks
        :param offset:<int> Starting position in the landmarks array for either left or right eye
        """
        a = ((landmarks.part(1 + offset).x - landmarks.part(5 + offset).x) ** 2 +
             (landmarks.part(1 + offset).y - landmarks.part(5 + offset).y) ** 2) ** (1 / 2)
        b = ((landmarks.part(2 + offset).x - landmarks.part(4 + offset).x) ** 2 +
             (landmarks.part(2 + offset).y - landmarks.part(4 + offset).y) ** 2) ** (1 / 2)
        c = ((landmarks.part(0 + offset).x - landmarks.part(3 + offset).x) ** 2 +
             (landmarks.part(0 + offset).y - landmarks.part(3 + offset).y) ** 2) ** (1 / 2)
        return (a + b) / (2.0 * c)

    @Slot()
    def check_frame(self):
        """
        Check to see if there is a frame available to be read from the video source
        """
        success, frame = self.cap.read()
        if success:
            self.process_frame(frame)
        return success

    def train_svm(self):
        """
        Train the blink support vector machine using a dataset
        """
        # Load and preprocess data
        X, y = self.load_data()
        X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=0, test_size=0.1, shuffle=True)

        # Train SVM
        self.blink_svm = svm.SVC(kernel='rbf', C=1, gamma='scale')
        self.blink_svm.fit(X_train, y_train)

        # Test SVM
        y_pred = self.blink_svm.predict(X_test)
        print(confusion_matrix(y_test, y_pred))
        print(classification_report(y_test, y_pred))

        # Save SVM
        with open('resources/blink_model.pk1', 'wb') as f:
            pickle.dump(self.blink_svm, f)

    @staticmethod
    def load_data():
        """
        Load eye aspect ratio data from a text file for support vector machine training
        """
        x = []
        y = []
        ear = []
        label = []
        with open("resources/datasets/labels_eyeblink8.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip()
                line = line.split(":")
                y.append(line[3])
        with open("resources/datasets/ear_output_eyeblink8.txt", "r") as file:
            lines = file.readlines()
            for line in lines:
                line = line.rstrip()
                line = line.split(":")
                x.append(float(line[1]))
            last_blink = 0  # The index that a blink last occurred
            for i in range(BlinkDetector.EAR_FEATURE_SIZE_HALF, len(x) - BlinkDetector.EAR_FEATURE_SIZE_HALF):
                temp = []
                for j in range(-BlinkDetector.EAR_FEATURE_SIZE_HALF, BlinkDetector.EAR_FEATURE_SIZE_HALF + 1):
                    temp.append(x[i-j])
                if y[i] == 'X' and last_blink + BlinkDetector.EAR_FEATURE_SIZE < i:
                    ear.append(temp)
                    label.append(y[i])
                elif y[i] == 'C':
                    last_blink = i
                    ear.append(temp)
                    label.append(y[i])
        return ear, label

    def calc_data(self):
        """
        Calculates eye aspect ratio for each frame from a video file
        """
        with open("ear_output.txt", "w") as file:
            while True:
                ret = self.check_frame()
                if not ret:
                    break
                string = str(self.frame_count - 1) + ":" + str(self.ear_feature[0])
                string += "\n"
                file.write(string)
                cv2.waitKey(5)

    def detect_blinks_threshold(self):
        """
        Detects a blink using thresholding technique
        """
        if len(self.ear_feature) >= 2:
            if self.ear_feature[0] > BlinkDetector.EAR_THRESHOLD > self.ear_feature[1]:
                print("blink")
                self.blink_detected.emit()

    def detect_blinks_svm(self):
        """
        Feeds a vector of eye aspect ratio values to a support vector machine to classify blinks
        """
        if len(self.ear_feature) == BlinkDetector.EAR_FEATURE_SIZE and \
                self.frame_count > self.last_blink_frame + BlinkDetector.EAR_FEATURE_SIZE:
            if self.blink_svm.predict([self.ear_feature]) == 'C':
                print("blink")
                self.blink_detected.emit()
                self.last_blink_frame = self.frame_count

    def process_frame(self, frame):
        """
        Applies face detection, landmark detection, and blink detection on a retrieved frame
        """
        self.frame_count += 1
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_small = cv2.resize(gray, (0, 0), fx=1.0 / BlinkDetector.DOWNSIZE_RATIO,
                                fy=1.0 / BlinkDetector.DOWNSIZE_RATIO)
        if self.frame_count % BlinkDetector.SKIP_FRAMES == 0 or len(self.faces) == 0:
            self.faces = self.face_detector(gray_small, 0)  # up-sample 0 times (less accurate, faster)
        if len(self.faces) >= 1:
            face = self.scale_dlib_rect(self.faces[0], BlinkDetector.DOWNSIZE_RATIO)
            landmarks = self.landmark_detector(gray, face)
            ear_left = self.calc_ear(landmarks, BlinkDetector.LEFT_EYE_OFFSET)
            ear_right = self.calc_ear(landmarks, BlinkDetector.RIGHT_EYE_OFFSET)
            self.ear_feature.insert(0, (ear_left + ear_right) / 2.0)
            self.detect_blinks_svm()
            if self.draw_mode:
                for i in range(landmarks.num_parts):
                    cv2.circle(gray, (landmarks.part(i).x, landmarks.part(i).y), 1, (0, 255, 255), -1)
            self.face_detected.emit(True)
        else:
            self.ear_feature.insert(0, 0.5)
            self.face_detected.emit(False)
        if len(self.ear_feature) >= BlinkDetector.EAR_FEATURE_SIZE:
            self.ear_feature.pop()
        self.frames_per_sec = self.frame_count / (time.time() - self.start_time)
        if self.draw_mode:
            cv2.imshow("Output", gray)

# ----------------------------------------------------------------------------------------------------------------------
# Example class uses


# Training SVM
# blink_detector = BlinkDetector(0, True)
# blink_detector.train_svm()

# Getting training data from a video file
# blink_detector = BlinkDetector("C:/eyeblink8/11/27122013_154548_cam.avi", True)
# blink_detector.calc_data()

# Normal operation
# Blink_detector = BlinkDetector(0, True)
# while True:
#    blink_detector.check_frame()
#    cv2.waitKey(5)
