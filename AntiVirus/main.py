import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QFileDialog
from datetime import datetime
import os
import shutil

class AntiVirusApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AntiVirus Application")
        self.setGeometry(100, 100, 600, 400)

        # Layout and Widgets
        self.layout = QVBoxLayout()

        self.scan_button = QPushButton("Scan Files")
        self.scan_button.clicked.connect(self.scan_files)
        self.layout.addWidget(self.scan_button)

        self.view_log_button = QPushButton("View Quarantine Log")
        self.view_log_button.clicked.connect(self.view_quarantine_log)
        self.layout.addWidget(self.view_log_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        self.layout.addWidget(self.result_area)

        # Set central widget
        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)

    def scan_files(self):
        # Open file dialog to select a file
        file_path, _ = QFileDialog.getOpenFileName(self, "Select File to Scan")
        if file_path:
            # Simulate scanning (replace with actual scanning logic)
            file_hash = self.calculate_file_hash(file_path)
            if self.is_malicious(file_hash):
                self.quarantine_file(file_path)
                self.result_area.setText(f"File '{file_path}' is malicious and has been quarantined.")
            else:
                self.result_area.setText(f"File '{file_path}' is clean.")

    def view_quarantine_log(self):
        # Display the contents of quarantine_log.txt
        log_path = os.path.join("AntiVirus", "quarantine", "quarantine_log.txt")
        if os.path.exists(log_path):
            with open(log_path, "r") as log_file:
                self.result_area.setText(log_file.read())
        else:
            self.result_area.setText("No quarantine log found.")

    def calculate_file_hash(self, file_path):
        # Calculate MD5 hash of the file
        import hashlib
        with open(file_path, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()

    def is_malicious(self, file_hash):
        # Check if the file hash exists in signatures.txt
        signatures_path = os.path.join("AntiVirus", "signatures.txt")
        if os.path.exists(signatures_path):
            with open(signatures_path, "r") as sig_file:
                signatures = sig_file.read().splitlines()
                return file_hash in signatures
        return False

    def quarantine_file(self, file_path):
        # Move the file to the quarantine folder and log it
        quarantine_folder = os.path.join("AntiVirus", "quarantine")
        os.makedirs(quarantine_folder, exist_ok=True)

        file_name = os.path.basename(file_path)
        quarantined_path = os.path.join(quarantine_folder, file_name)
        shutil.move(file_path, quarantined_path)

        # Log the quarantined file
        log_path = os.path.join(quarantine_folder, "quarantine_log.txt")
        with open(log_path, "a") as log_file:
            log_file.write(f"{file_name}, {file_path}, {datetime.now()}\n")

# Run the application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AntiVirusApp()
    window.show()
    sys.exit(app.exec_())