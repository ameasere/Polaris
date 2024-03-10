from PySide6.QtCore import Qt, QRectF, QTimer, Signal, QObject, QThread
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QWidget
import socket
import time

class NetworkWorker(QObject):
    finished = Signal()
    progress_signal = Signal(str)

    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            statistics_hsm_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                statistics_hsm_connection.connect(("192.168.0.212", 26556))
                statistics = str(statistics_hsm_connection.recv(1024))
                self.progress_signal.emit(statistics)
                statistics_hsm_connection.close()
                time.sleep(1)
            except Exception as e:
                print(e)
                time.sleep(1)
                continue
        self.finished.emit()

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

        self.worker = NetworkWorker()
        self.thread = QThread()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress_signal.connect(self.update_graph)
        self.thread.start()

    def update_graph(self, statistics):
        # Fetch CPU usage
        statistics_array = statistics.replace("polaris://", "").split("/")
        cpu_statistics = statistics_array[0]
        cpu_percent = float(cpu_statistics.split(":")[1])
        current_cpu = str(int(cpu_percent)) + "%"
        print(f"CPU: {current_cpu}")
        cpu_x = len(self.scene.items()) * 5
        # Calculate the height of the bar based on CPU percentage
        cpu_bar_height = (self.graph_view.height() - 5) * (cpu_percent / 100)
        if cpu_bar_height < 1:
            cpu_bar_height = 1
        # Sort the items based on their x-coordinate
        cpu_items = sorted(self.scene.items(), key=lambda x: x.rect().x())
        # Remove the first item if the total width of all bars exceeds the view width
        while len(cpu_items) * 5 > self.graph_view.width() - 30:
            item = cpu_items.pop(0)
            self.scene.removeItem(item)
            for item in cpu_items:
                item.setRect(
                    QRectF(item.rect().x() - 5, item.rect().y(), item.rect().width(), item.rect().height()))
            cpu_x = (len(cpu_items) * 5) - 5

        # Draw a bar representing CPU usage
        try:
            cpu_bar = QGraphicsRectItem(cpu_x, self.graph_view.height() - cpu_bar_height, 5, cpu_bar_height)
            # Set brush with 9e77ed
            cpu_bar.setBrush(QColor("#9e77ed"))
            self.scene.addItem(cpu_bar)
            self.scene.update(self.scene.sceneRect())
            print(f"Bar added at x: {cpu_x}, height: {cpu_bar_height}")

        except Exception as e:
            print(e)

if __name__ == "__main__":
    import sys
    from PySide6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    monitor = SystemMonitor()
    monitor.show()
    sys.exit(app.exec())
