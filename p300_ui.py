
import sys
import numpy as np
from PyQt5.QtCore import pyqtProperty, QCoreApplication, QObject, QUrl, QTimer, QRect
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine


# This is the type that will be registered with QML.  It must be a
# sub-class of QObject.
class RandomBox(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialise the value of the properties.
        self._name = ''
        self._beta = 500
    
        self.inter_timer = QTimer(self)
        self.timer.connect(self.timer_callback)

        self.disp_time = QTimer(self)
        self.disp_time.connect(self.blank_rect)
        self.rect = QRect(400, 400, 200, 200)
        self.rect.setStyleSheet("background-color : white")


    # Define the getter of the 'name' property.  The C++ type of the
    # property is QString which Python will convert to and from a string.
    @pyqtProperty('QString')
    def name(self):
        return self._name

    # Define the setter of the 'name' property.
    @name.setter
    def name(self, name):
        self._name = name

    # Define the getter of the 'shoeSize' property.  The C++ type and
    # Python type of the property is int.
    @pyqtProperty(int)
    def beta(self):
        return self._beta

    # Define the setter of the 'shoeSize' property.
    @beta.setter
    def beta(self, beta):
        self._beta = beta

    def show_rect(self):
        # bold rect
        self.rect.setStyleSheet("background-color : black")
        self.inter_timer.stop()
        self.disp_time.start(30)
    
    def blank_rect(self):
        self.rect.setStyleSheet("background-color : white")
        self.disp_time.stop()
        inter = np.random.exponential(scale=self._beta)
        self.inter_timer.start(inter)


        

# Register the Python type.  Its URI is 'People', it's v1.0 and the type
# will be called 'Person' in QML.
qmlRegisterType(RandomBox, 'RandomBox', 1, 0, 'RandomBox')


# Create the application instance.
app = QCoreApplication(sys.argv)

# Create a QML engine.
engine = QQmlEngine()

# Create a component factory and load the QML script.
component = QQmlComponent(engine)
component.loadUrl(QUrl('p300.qml'))

# Create an instance of the component.
person = component.create()

component.show()