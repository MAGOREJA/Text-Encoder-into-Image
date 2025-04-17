import sys
import os
import psutil
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QThread, pyqtSignal
from pynput import keyboard


class KeyloggerDetector(QThread):
    detection_signal = pyqtSignal(str)  # Signal to update the UI with detection results

    def __init__(self):
        super().__init__()
        self.suspicious_processes = ["keylogger.exe", "spyware.exe"]  # Example signatures
        self.detected = False

    def scan_for_keylogger_signatures(self):
        # Check for suspicious processes
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.info['name'] in self.suspicious_processes:
                    self.detected = True
                    return f"Suspicious process detected: {proc.info['name']}"
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return "No suspicious processes found."

    def monitor_system_hooks(self):
        # Monitor for unusual keyboard activity
        def on_press(key):
            if key == keyboard.Key.ctrl_l:  # Example: Detect specific key combinations
                self.detected = True
                self.detection_signal.emit("Suspicious key activity detected!")
                return False  # Stop listener

        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()

    def run(self):
        # Step 1: Scan for known keylogger signatures
        result = self.scan_for_keylogger_signatures()
        if self.detected:
            self.detection_signal.emit(result)
            return

        # Step 2: Monitor system hooks or suspicious input events
        self.monitor_system_hooks()

        # Step 3: Update the label text based on the detection result
        if not self.detected:
            self.detection_signal.emit("No suspicious activity detected.")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Keylogger Detector")
        self.setGeometry(100, 100, 400, 200)

        # UI Elements
        self.label = QLabel("Click 'Start Detection' to begin.", self)
        self.label.setWordWrap(True)
        self.start_button = QPushButton("Start Detection", self)
        self.start_button.clicked.connect(self.start_detection)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_button)
        self.setLayout(layout)

        # Keylogger Detector
        self.detector = KeyloggerDetector()
        self.detector.detection_signal.connect(self.update_label)

    def start_detection(self):
        self.label.setText("Detecting suspicious activity...")
        self.detector.start()

    def update_label(self, message):
        self.label.setText(message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())