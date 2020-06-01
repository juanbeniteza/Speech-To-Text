import sys
import os
import pyttsx3
import speech_recognition as sr
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QTextEdit, QLineEdit, QFileDialog, QApplication, QTabWidget, QCheckBox


FONT = QFont("Open Sans", 22, weight=75)
FONT.setBold(True)


class Window(QTabWidget):

    def __init__(self):
        super().__init__()
        self.setMaximumSize(430, 340)
        self.setMinimumSize(430, 340)
        self.addTab(TextTab(), 'Text')
        self.addTab(VoiceTab(), 'Voice')
        self.setWindowTitle('Text to Speech with Python')


class TextTab(QWidget):

    def __init__(self):
        super().__init__()
        acceptButton = QPushButton('Accept', self)
        acceptButton.setGeometry(QRect(310, 260, 85, 27))
        acceptButton.clicked.connect(self.callTextToSpeech) # Event on accept button

        self.textArea = QTextEdit('Write here...', self)
        self.textArea.setGeometry(QRect(20, 70, 371, 181))

        label = QLabel("Text to Speech", self)
        label.setGeometry(QRect(60, 10, 301, 31))
        label.setFont(FONT)
        label.setAlignment(Qt.AlignCenter)

    def callTextToSpeech(self):
        text = self.textArea.toPlainText()
        textToSpeech(text)


class VoiceTab(QWidget):

    def __init__(self):
        super().__init__()
        acceptButton = QPushButton('Accept', self)
        acceptButton.setGeometry(QRect(320, 100, 85, 27))  # (X, Y, W, H)
        acceptButton.clicked.connect(self.callSpeechToText) # Event on accept button

        searchButton = QPushButton('Find', self)
        searchButton.setGeometry(QRect(10, 60, 85, 27))
        searchButton.clicked.connect(self.openFileExplorer) # Event on search button

        self.pathInput = QLineEdit(self)
        self.pathInput.setGeometry(QRect(100, 60, 305, 27))

        self.checkBox = QCheckBox('You should use your mic instead!', self)
        self.checkBox.setGeometry(QRect(10, 100, 300, 20))

        self.textArea = QTextEdit(self)
        self.textArea.setGeometry(QRect(15, 140, 390, 160))
        self.textArea.setReadOnly(True)

        label = QLabel("Speech to Text", self)
        label.setGeometry(QRect(60, 10, 301, 31))
        label.setFont(FONT)
        label.setAlignment(Qt.AlignCenter)

    def setPathInput(self, value):
        self.pathInput.setText(value)

    def openFileExplorer(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "Open file")

        if filePath:
            self.setPathInput(filePath)

    def callSpeechToText(self):
        useMic = self.checkBox.isChecked()
        pathFile = None

        if not useMic:
            pathFile = os.path.join(os.path.dirname(
                os.path.realpath(__file__)), str(self.pathInput.text()))

        self.textArea.setPlainText(SpeechToText(pathFile))


def textToSpeech(text):
    """
    params: text -> str

    Speech the text passed
    """
    
    engine = pyttsx3.init()
    engine.setProperty('rate', 100)
    engine.say(text)
    engine.runAndWait()


def SpeechToText(pathFile=None):
    """
    params: pathFile -> str
    returns: audio converted to string
    """

    ouput = ''
    r = sr.Recognizer()
    if pathFile:
        # with File as source:
        with sr.AudioFile(pathFile) as source:
            audio = r.record(source)
            try:
                ouput = r.recognize_google(audio)
            except Exception:
                ouput = 'Sorry, we were not able to understand you!'
    else:
        # with Microphone() as source:
        with sr.Microphone() as source:
            audio = r.listen(source)
            try:
                ouput = r.recognize_google(audio)
            except Exception:
                ouput = 'Sorry, we were not able to understand you!'
    return f'You said: \n{ouput}'


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
