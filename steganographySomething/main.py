from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QLabel, QFileDialog, QWidget
)
from PyQt5.QtCore import Qt
from PIL import Image
import numpy as np
import sys


class SteganographyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Steganography App")
        self.setGeometry(100, 100, 600, 400)

        # Main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Label
        self.label = QLabel("Enter text to encode or decode:")
        self.layout.addWidget(self.label)

        # Text area
        self.text_area = QTextEdit()
        self.layout.addWidget(self.text_area)

        # Encode button
        self.encode_button = QPushButton("Encode Text into Image")
        self.encode_button.clicked.connect(self.encode_text)
        self.layout.addWidget(self.encode_button)

        # Decode button
        self.decode_button = QPushButton("Decode Text from Image")
        self.decode_button.clicked.connect(self.decode_text)
        self.layout.addWidget(self.decode_button)

    def encode_text(self):
        # Get the text to encode
        text = self.text_area.toPlainText()
        if not text:
            self.text_area.setText("Please enter text to encode.")
            return

        # Open the image file
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Image File", "", "Images (*.png *.jpg *.bmp)")
        if not file_name:
            self.text_area.setText("No image file selected.")
            return

        image = Image.open(file_name)
        image_data = np.array(image)

        # Convert text to binary
        binary_text = ''.join(format(ord(char), '08b') for char in text)
        binary_text += '1111111111111110'  # Delimiter to indicate end of text

        # Flatten the image array and modify LSBs
        flat_image = image_data.flatten()
        if len(binary_text) > len(flat_image):
            self.text_area.setText("Text is too long to encode in the selected image.")
            return

        for i in range(len(binary_text)):
            flat_image[i] = (flat_image[i] & 254) | int(binary_text[i])
        
        # Reshape the modified flat array back to the original image shape
        encoded_image_data = flat_image.reshape(image_data.shape)
        encoded_image = Image.fromarray(encoded_image_data.astype('uint8'))

        # Save the encoded image
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Encoded Image", "", "Images (*.png *.bmp)")
        if save_path:
            encoded_image.save(save_path)
            self.text_area.setText(f"Text successfully encoded and saved to {save_path}.")
        else:
            self.text_area.setText("Encoding canceled.")

    def decode_text(self):
        # Open the steganographic image file
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Encoded Image File", "", "Images (*.png *.jpg *.bmp)")
        if not file_name:
            self.text_area.setText("No image file selected.")
            return

        image = Image.open(file_name)
        image_data = np.array(image)

        # Extract LSBs from the image
        flat_image = image_data.flatten()
        binary_text = ''.join(str(flat_image[i] & 1) for i in range(len(flat_image)))

        # Split binary data at the delimiter
        delimiter = '1111111111111110'
        if delimiter in binary_text:
            binary_text = binary_text[:binary_text.index(delimiter)]
        else:
            self.text_area.setText("No hidden text found in the image.")
            return

        # Convert binary data to text
        decoded_text = ''.join(chr(int(binary_text[i:i+8], 2)) for i in range(0, len(binary_text), 8))
        self.text_area.setText(decoded_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SteganographyApp()
    window.show()
    sys.exit(app.exec_())