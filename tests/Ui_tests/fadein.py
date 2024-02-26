from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QGraphicsOpacityEffect
from PySide6.QtCore import QPropertyAnimation, QEasingCurve


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.button = QPushButton("Test Button")
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)

        self.opacity_effect = QGraphicsOpacityEffect(self.button)
        self.button.setGraphicsEffect(self.opacity_effect)
        self.opacity_effect.setOpacity(0)

        self.animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)

        self.button.clicked.connect(self.fade_in)

    def fade_in(self):
        self.animation.start()


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
