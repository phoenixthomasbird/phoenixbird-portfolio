import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QHBoxLayout, QLineEdit, QPushButton, QTextEdit,
    QLabel, QProgressBar, QSplitter
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QColor, QPalette

from agent import run_agent


# ── Worker Thread ─────────────────────────────────────────────────────────────
# Lives in a separate thread so the UI stays responsive while the agent runs.

class AgentWorker(QThread):
    # Signals are the ONLY way to talk to the UI from a worker thread
    log_message = pyqtSignal(str)    # emitted for each progress line
    answer_ready = pyqtSignal(str)   # emitted once when agent finishes
    error_occurred = pyqtSignal(str) # emitted if something goes wrong

    def __init__(self, question: str):
        super().__init__()
        self.question = question

    def run(self):
        """This method runs in the worker thread, never on the main thread."""
        try:
            # Pass our signal emitter as the on_log callback.
            # When the agent calls on_log("some message"),
            # it actually calls self.log_message.emit("some message"),
            # which safely crosses the thread boundary to the UI.
            answer = run_agent(
                self.question,
                on_log=self.log_message.emit
            )
            self.answer_ready.emit(answer)
        except Exception as e:
            self.error_occurred.emit(str(e))


# ── Main Window ───────────────────────────────────────────────────────────────

class AgentWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.worker = None
        self.setWindowTitle("Research Agent")
        self.setMinimumSize(900, 700)
        self._build_ui()
        self._apply_styles()

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # ── Input row ──────────────────────────────────────────
        input_row = QHBoxLayout()

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText(
            "Ask anything... e.g. What caused the 2008 financial crisis?"
        )
        self.question_input.setFixedHeight(40)
        # Let user hit Enter to run
        self.question_input.returnPressed.connect(self.run_agent)

        self.run_button = QPushButton("Run")
        self.run_button.setFixedSize(80, 40)
        self.run_button.clicked.connect(self.run_agent)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setFixedSize(80, 40)
        self.stop_button.setEnabled(False)
        self.stop_button.clicked.connect(self.stop_agent)

        input_row.addWidget(self.question_input)
        input_row.addWidget(self.run_button)
        input_row.addWidget(self.stop_button)
        layout.addLayout(input_row)

        # ── Progress bar ───────────────────────────────────────
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)   # 0,0 = indeterminate (spinning)
        self.progress.setFixedHeight(4)
        self.progress.setVisible(False)
        layout.addWidget(self.progress)

        # ── Splitter: log on top, answer below ─────────────────
        splitter = QSplitter(Qt.Vertical)

        # Log panel
        log_container = QWidget()
        log_layout = QVBoxLayout(log_container)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_layout.addWidget(QLabel("Agent activity"))
        self.log_view = QTextEdit()
        self.log_view.setReadOnly(True)
        self.log_view.setFont(QFont("Courier", 11))
        log_layout.addWidget(self.log_view)
        splitter.addWidget(log_container)

        # Answer panel
        answer_container = QWidget()
        answer_layout = QVBoxLayout(answer_container)
        answer_layout.setContentsMargins(0, 0, 0, 0)
        answer_layout.addWidget(QLabel("Answer"))
        self.answer_view = QTextEdit()
        self.answer_view.setReadOnly(True)
        self.answer_view.setFont(QFont("Georgia", 13))
        answer_layout.addWidget(self.answer_view)
        splitter.addWidget(answer_container)

        splitter.setSizes([300, 300])
        layout.addWidget(splitter)

        # ── Status bar ─────────────────────────────────────────
        self.statusBar().showMessage("Ready")

    def _apply_styles(self):
        self.setStyleSheet("""
            QMainWindow { background: #1e1e2e; }
            QWidget     { background: #1e1e2e; color: #cdd6f4; }

            QLineEdit {
                background: #313244;
                border: 1px solid #45475a;
                border-radius: 6px;
                padding: 0 10px;
                color: #cdd6f4;
                font-size: 14px;
            }
            QLineEdit:focus { border-color: #89b4fa; }

            QPushButton {
                background: #313244;
                border: 1px solid #45475a;
                border-radius: 6px;
                color: #cdd6f4;
                font-size: 13px;
            }
            QPushButton:hover   { background: #45475a; }
            QPushButton:pressed { background: #585b70; }
            QPushButton:disabled { color: #585b70; }

            QTextEdit {
                background: #181825;
                border: 1px solid #313244;
                border-radius: 6px;
                padding: 8px;
                color: #cdd6f4;
            }

            QLabel { color: #a6adc8; font-size: 12px; margin-bottom: 4px; }

            QProgressBar {
                background: #313244;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk { background: #89b4fa; border-radius: 2px; }

            QSplitter::handle { background: #313244; height: 2px; }
            QStatusBar { color: #a6adc8; font-size: 12px; }
        """)

    # ── Agent control ──────────────────────────────────────────────────────────

    def run_agent(self):
        question = self.question_input.text().strip()
        if not question:
            return

        # Reset UI state
        self.log_view.clear()
        self.answer_view.clear()
        self.run_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress.setVisible(True)
        self.statusBar().showMessage("Agent running...")

        # Create and wire up the worker
        self.worker = AgentWorker(question)
        self.worker.log_message.connect(self.on_log)
        self.worker.answer_ready.connect(self.on_answer)
        self.worker.error_occurred.connect(self.on_error)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def stop_agent(self):
        if self.worker and self.worker.isRunning():
            self.worker.terminate()  # Force-stops the thread
            self.on_log("[Stopped by user]")
            self.on_finished()

    # ── Signal handlers (always run on main thread) ────────────────────────────

    def on_log(self, message: str):
        """Called each time the agent emits a progress line."""
        self.log_view.append(message)
        # Auto-scroll to bottom
        scrollbar = self.log_view.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def on_answer(self, answer: str):
        """Called once when the agent finishes."""
        self.answer_view.setPlainText(answer)
        self.statusBar().showMessage("Done.")

    def on_error(self, error: str):
        """Called if the agent throws an exception."""
        self.log_view.append(f"\n[ERROR] {error}")
        self.statusBar().showMessage(f"Error: {error}")

    def on_finished(self):
        """Called when the worker thread exits, success or not."""
        self.run_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress.setVisible(False)


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Research Agent")
    window = AgentWindow()
    window.show()
    sys.exit(app.exec_())
