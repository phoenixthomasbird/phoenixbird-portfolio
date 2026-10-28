
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit

class MainWindow(QWidget):
    def __init__(self):
        super().__init__() 
        self.setWindowTitle("My First GUI")
        self.resize(300,200)

        self.label = QLabel("Hello!")
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type something...")

        submit_button = QPushButton("Subtmit")
        submit_button.clicked.connect(self.on_submit)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_box)
        layout.addWidget(submit_button)
        self.setLayout(layout)

    def on_submit(self):
        text = self.input_box.text()
        self.label.setText(f"You typed: {text}")

app = QApplication(sys.argv) #manages the app-wide event loop, settings, etc.
window = MainWindow()             #QWidget = base class for any visual element
window.show()
sys.exit(app.exec_())            #starts the event loop; blocks until app closes