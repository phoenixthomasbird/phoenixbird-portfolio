
import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, 
    QVBoxLayout, QHBoxLayout, QLineEdit
)

import practice_3
print(__name__)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My First GUI")
        self.resize(300, 200)

        self.label = QLabel("Hello!")
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type something...")

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.on_submit)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_box)
        layout.addWidget(submit_button)
        self.setLayout(layout)

    def on_submit(self):
        text = self.input_box.text()
        if text:
            self.label.setText(f"{text}")
        else:
            self.label.setText("Please enter something!")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
    