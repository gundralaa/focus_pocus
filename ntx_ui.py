import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QTimer, QRect, QSize
from PyQt5.QtGui import QPaintEvent
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
import PyQt5

class UI(QMainWindow):

    def __init__(self, word1 = 'Word 1', word2 = 'Word 2', word3 = 'Word 3', word4 = 'Word 4'):
        super(UI, self).__init__()
        self.timer1, self.timer2, self.timer3, self.timer4 = None, None, None, None
        self.button1, self.button2, self.button3, self.button4 = None, None, None, None
        self.word1, self.word2, self.word3, self.word4 = word1, word2, word3, word4
        self.frame1, self.frame2, self.frame3, self.frame4 = False, False, False, False
        self.initUI()

    def initUI(self):
        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Background, QtCore.Qt.black)
        self.setPalette(palette)

        rect1 = QRect(10, 10, 380, 380)
        rect2 = QRect(10, 410, 380, 380)
        rect3 = QRect(410, 10, 380, 380)
        rect4 = QRect(410, 410, 380, 380)
        painter = QtGui.QPainter(self)
        painter.drawRect(rect1)
        painter.drawRect(rect2)
        painter.drawRect(rect3)
        painter.drawRect(rect4)

        self.button1 = QPushButton(self.word1, self)
        self.button1.resize(380, 380)
        self.button1.move(10, 10)
        self.button1.setStyleSheet("background-color : white")

        self.button2 = QPushButton(self.word2, self)
        self.button2.resize(380, 380)
        self.button2.move(410, 10)
        self.button2.setStyleSheet("background-color : white")

        self.button3 = QPushButton(self.word3, self)
        self.button3.resize(380, 380)
        self.button3.move(10, 410)
        self.button3.setStyleSheet("background-color : white")

        self.button4 = QPushButton(self.word4, self)
        self.button4.resize(380, 380)
        self.button4.move(410, 410)
        self.button4.setStyleSheet("background-color : white")

        self.resize(800, 800)
        self.setWindowTitle('Game')
        
        self.timer1 = QtCore.QTimer()
        self.timer1.setSingleShot(True)
        self.timer1.timeout.connect(self.c1)

        self.timer2 = QtCore.QTimer()
        self.timer2.setSingleShot(True)
        self.timer2.timeout.connect(self.c2)

        self.timer3 = QtCore.QTimer()
        self.timer3.setSingleShot(True)
        self.timer3.timeout.connect(self.c3)

        self.timer4 = QtCore.QTimer()
        self.timer4.setSingleShot(True)
        self.timer4.timeout.connect(self.c4)

    def c1(self):
        self.button4.setStyleSheet("background-color : white")
        self.button1.setStyleSheet("background-color : blue")
        self.frame4 = False
        self.frame1 = True
        print(self.get_word())
        self.timer2.start(1000)

    def c2(self):
        self.button1.setStyleSheet("background-color : white")
        self.button2.setStyleSheet("background-color : blue")
        self.frame1 = False
        self.frame2 = True
        print(self.get_word())
        self.timer3.start(1000)

    def c3(self):
        self.button2.setStyleSheet("background-color : white")
        self.button3.setStyleSheet("background-color : blue")
        self.frame2 = False
        self.frame3 = True
        print(self.get_word())
        self.timer4.start(1000)

    def c4(self):
        self.button3.setStyleSheet("background-color : white")
        self.button4.setStyleSheet("background-color : blue")
        self.frame3 = False
        self.frame4 = True
        print(self.get_word())
        self.set_words("This", "is", "finally", "working")
        self.button1.setText(self.word1)
        self.button2.setText(self.word2)
        self.button3.setText(self.word3)
        self.button4.setText(self.word4)
        self.timer1.start(1000)
    
    def set_words(self, word1, word2, word3, word4):
        self.word1, self.word2, self.word3, self.word4 = word1, word2, word3, word4

    def get_word(self):
        if self.frame1:
            return self.word1
        if self.frame2:
            return self.word2
        if self.frame3:
            return self.word3
        if self.frame4:
            return self.word4

def main():

   app = PyQt5.QtWidgets.QApplication([])
   visuals = UI()
   visuals.show()
   visuals.timer1.start(1000)
   
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()
