# -*- coding: utf-8 -*-

from PyQt4.QtCore import * #Importamos modulos necesarios para la interfaz grafica
from PyQt4.QtGui import *


class Widget(QTabWidget):

    fichero_actual = ""
    def setupUi(self, TabWidget):

        TabWidget.resize(430, 340)
        TabWidget.setMaximumSize(430, 340)
        TabWidget.setMinimumSize(430, 340)
        #Pestaña 1
        tab = QWidget()
        Aceptar1 = QPushButton(tab)
        Aceptar1.setText("Aceptar")
        Aceptar1.setGeometry(QRect(310, 260, 85, 27))
        Aceptar1.setObjectName("Aceptar1")
        self.textEdit = QTextEdit(tab)
        self.textEdit.setGeometry(QRect(20, 70, 371, 181))
        self.textEdit.setObjectName(("lineEdit1"))
        label_3 = QLabel(tab)
        label_3.setGeometry(QRect(20, 50, 271, 17))
        label_3.setObjectName("label_3")
        label_3.setText("Escriba aqui lo que quiera escuchar")
        self.connect(Aceptar1, SIGNAL("clicked()"), self.text_to_speech) # Evento al clickear en aceptar
        label = QLabel(tab)
        label.setText("Text To Speech")
        label.setGeometry(QRect(60, 10, 301, 31))
        font = QFont()
        font.setFamily(("Noto Sans Mono CJK SC"))
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        label.setObjectName(("label"))
        TabWidget.addTab(tab, "")
        TabWidget.setTabText(TabWidget.indexOf(tab), "Texto")

        # Pestaña 2
        tab1 = QWidget()
        self.textEdit2 = QTextEdit(tab1)
        self.textEdit2.setGeometry(QRect(10, 140, 391, 161))
        self.textEdit2.setObjectName(("lineEdit2"))
        self.textEdit2.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignTop)
        self.textEdit2.setReadOnly(True)
        Aceptar2 = QPushButton(tab1)
        Aceptar2.setText("Aceptar")
        Aceptar2.setGeometry(QRect(310, 100, 85, 27))
        Aceptar2.setObjectName(("Aceptar2"))
        self.connect(Aceptar2, SIGNAL("clicked()"), self.speech_to_text) #Evento al clickear en aceptar
        Buscar = QPushButton(tab1)
        Buscar.setText("Buscar")
        Buscar.setGeometry(QRect(10, 60, 85, 27))
        Buscar.setObjectName(("Buscar"))
        self.connect(Buscar, SIGNAL("clicked()"), self.abrir) #Evento al clickear en buscar
        self.Ruta = QLineEdit(tab1)
        self.Ruta.setGeometry(QRect(100, 60, 301, 27))
        self.Ruta.setObjectName(("Ruta"))

        label_2 = QLabel(tab1)
        label_2.setText("Speech To Text")
        label_2.setGeometry(QRect(40, 10, 331, 31))
        font = QFont()
        font.setFamily(("Noto Sans Mono CJK SC"))
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        label_2.setFont(font)
        label_2.setAlignment(Qt.AlignCenter)
        label_2.setObjectName(("label_2"))
        label_4 = QLabel(tab1)
        label_4.setGeometry(QRect(10, 110, 291, 17))
        label_4.setObjectName(("label_4"))
        label_4.setText("El texto se mostrara aqui")
        TabWidget.addTab(tab1, "")
        TabWidget.setTabText(TabWidget.indexOf(tab1), "Voz")
        TabWidget.setWindowTitle("Proyecto IA")


    def text_to_speech(self): # Funcion para pasar de texto a voz
        from gtts import gTTS # Importamos los modulos necesarios
        shost = self.textEdit.toPlainText()  # Obtenemos el texto que pasaremos a voz
        print shost
        tts = gTTS(text = str(shost), lang='es') # Llamamos al metodo el cual convierto el texto a voz
        tts.save("audio.mp3") # Guardamos el audio en un archivo mp3

        self.convertidor() # Llamamos a la funcion convertir para convertir el formato del anterior audio a .wav


    def abrir(self): # Funcion para abrir un buscador de archivos
        nombre_fichero = QFileDialog.getOpenFileName(self, "Abrir fichero", self.fichero_actual) # capturamos la ruta del fichero
        if nombre_fichero: # si existe ese archivo se realiza lo sigte
            self.fichero_actual = nombre_fichero # Copiamos la ruta a una variable
            print self.fichero_actual
            self.Ruta.setText(nombre_fichero) # Rellenamos la linea de texto con la  ruta del archivo


    def convertidor(self): # Funcion para convertir un archivo de audio .mp3 a .wav
        from pydub import AudioSegment # Importamos los modulos necesarios
        #AudioSegment.converter = "C:/ffmpeg/bin/ffmpeg.exe"
        sound = AudioSegment.from_mp3("audio.mp3")  # Tomamos los datos de un archivo mp3 y guardamos
        sound.export("aud.wav", format = "wav") # creamos el nuevo archivo de audio .wav
        print "Done"


    def speech_to_text(self): # Funcion para pasar de voz a texto
        print "Aqui"

        import speech_recognition as sr # Importamos los modulos necesarios
        from os import path
        AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), str(self.Ruta.text())) # Obtenemos el audio a convertir debe ser .wav

        r = sr.Recognizer() # Creamos una instacia de la clase Recognizer
        with sr.AudioFile(AUDIO_FILE) as source:
            audio = r.record(source)  # Leemos completamente el archivo de audio

        # recognize speech usando Google Speech Recognition
        try:
            # Llamamos al metodo de reconocimiento por google y le pasamos el audio
            salida = "Google dice: " + r.recognize_google(audio) # Guardamos la salida en una variable
        except sr.UnknownValueError: # Definimos excepciones que se puedan presentar
            salida = ("Google Speech Recognition no pudo entender el audio")
        except sr.RequestError as e:
            salida = ("no se pueden usar los servicios de Google Speech Recognition; {0}".format(e))


        # recognize speech usando WIT.AI Recognition

        WIT_AI_KEY = "COBIS4RA5JUJEIFUS3QTDWHSOY3L45YR"  # Wit.ai keys are 32-character uppercase alphanumeric strings


        try:
            # Llamamos al metodo de reconocimiento por wit y le pasamos el audio, y la key
           salida2 =  ("Wit.ai dice: " + r.recognize_wit(audio, key=WIT_AI_KEY)) # Guardamos la salida en una variable
        except sr.UnknownValueError: # Definimos excepciones que se puedan presentar
            salida2 = ("Wit.ai no pudo entender el audio")
        except sr.RequestError as e:
            salida2 = ("no se pueden usar los servicios de Wit.ai; {0}".format(e))

        self.textEdit2.setPlainText('--------- Transcripcion ---------' + '\n' + salida + '\n'
                            +  salida2)  # Imprimimos en el campo de texto las salidas
        print "Fin"




if __name__ == "__main__":  # Creamos el main del script
    import sys

    app =QApplication(sys.argv)
    TabWidget = QTabWidget()
    ui = Widget()
    ui.setupUi(TabWidget)
    TabWidget.show()
    sys.exit(app.exec_())
