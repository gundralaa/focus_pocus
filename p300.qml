import QtQuick 2.15
import QtQuick.Controls 2.15
import RandomBox 1.0

ApplicationWindow {
    visible: true
    width: 800
    height: 800
    title: "HelloApp"

    RandomBox {
        beta: 500
        name: "stim"
    }

    Text {
        anchors.centerIn: parent
        text: "Hello World"
        font.pixelSize: 24
    }

}