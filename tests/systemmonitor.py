from PySide6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QVBoxLayout, QWidget, \
    QGraphicsLineItem
from PySide6.QtCore import Qt, QTimer
import psutil


class SystemMonitor(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("System Monitor")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        self.graph_view = QGraphicsView()
        layout.addWidget(self.graph_view)

        self.scene = QGraphicsScene()
        self.graph_view.setScene(self.scene)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_graph)
        self.timer.start(1000)  # Update graph every second

    def update_graph(self):
        # Fetch CPU usage
        cpu_percent = psutil.cpu_percent()

        # Remove the first item if the scene width exceeds a certain value
        if self.scene.width() > self.graph_view.width():
            item = self.scene.items()[0]
            self.scene.removeItem(item)

        # Draw a line representing CPU usage
        line = QGraphicsLineItem(self.scene.width(), self.graph_view.height(), self.scene.width(),
                                 self.graph_view.height() - (cpu_percent * self.graph_view.height() / 10))
        self.scene.addItem(line)


if __name__ == "__main__":
    app = QApplication([])
    monitor = SystemMonitor()
    monitor.show()
    app.exec()
