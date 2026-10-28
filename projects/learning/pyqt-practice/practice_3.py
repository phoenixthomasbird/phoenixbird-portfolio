import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QLineEdit, QComboBox
)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My First GUI")
        self.resize(300, 250)

        self.label = QLabel("Hello")
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Type something...")

        self.dropdown = QComboBox()
        self.dropdown.addItems(["Greeting","Farewell","Question"])

        submit_button = QPushButton("Submit")
        submit_button.clicked.connect(self.on_submit)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.input_box)
        layout.addWidget(self.dropdown)
        layout.addWidget(submit_button)
        self.setLayout(layout)

    def on_submit(self):
        text = self.input_box.text()
        mode = self.dropdown.currentText()

        if not text:
            self.label.setText("Please enter something!")
            return

        if mode == "Greeting":
            self.label.setText(f"Hello, {text}!")
        elif mode == "Farewell":
            self.label.setText(f"Goodbye, {text}.")
        elif mode == "Question":
            self.label.setText(f"{text}?")

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
