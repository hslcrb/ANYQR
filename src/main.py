import sys
import os
import webbrowser
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QTabWidget, QTextEdit, 
                             QFileDialog, QMessageBox, QFrame, QSplitter, QColorDialog, QListWidget)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage, QKeySequence, QShortcut, QClipboard, QScreen
from PIL import ImageQt, Image
from qr_processor import QRProcessor

FRUTIGER_AERO_STYLE = """
QMainWindow {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #d4f0ff, stop: 1 #ffffff);
}
QTabWidget::pane {
    border: 1px solid #78c5ef;
    background: rgba(255, 255, 255, 0.7);
    border-radius: 12px;
}
QTabBar::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #e6f7ff, stop: 1 #b3e6ff);
    border: 1px solid #78c5ef;
    border-radius: 6px;
    padding: 10px 20px;
    margin-right: 4px;
    margin-bottom: -1px;
    color: #005a96;
    font-weight: bold;
}
QTabBar::tab:selected, QTabBar::tab:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffffff, stop: 1 #cceeff);
}
QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #68c7ff, stop: 0.5 #009cf1, stop: 0.51 #0087d8, stop: 1 #009cf1);
    border: 1px solid #005a96;
    border-radius: 15px;
    padding: 10px 20px;
    color: white;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #aee5ff, stop: 0.5 #27aff7, stop: 0.51 #19a1e8, stop: 1 #27aff7);
}
QLineEdit, QTextEdit, QListWidget {
    border: 2px solid #a3dcff;
    border-radius: 8px;
    padding: 6px;
    background-color: rgba(255, 255, 255, 0.85);
    selection-background-color: #009cf1;
}
QLabel {
    color: #1a4d80;
    font-size: 14px;
    font-weight: bold;
}
"""

class DropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setText("🌿 Drag and Drop Image Here\nor Paste (Ctrl+V) 🌿")
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #009cf1;
                border-radius: 15px;
                background-color: rgba(255, 255, 255, 0.6);
                color: #005a96;
                font-size: 18px;
                padding: 20px;
            }
            QLabel:hover {
                background-color: rgba(0, 156, 241, 0.1);
                border-color: #005a96;
            }
        """)
        self.setAcceptDrops(True)
        self.main_app = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage() or event.mimeData().hasUrls():
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage():
            image = event.mimeData().imageData()
            if self.main_app:
                self.main_app.process_qimage(image)
        elif event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls:
                path = urls[0].toLocalFile()
                if path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    if self.main_app:
                        self.main_app.process_image_file(path)

class AnyQRApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AnyQR - Super QR App (Frutiger Aero)")
        self.resize(850, 650)
        self.setStyleSheet(FRUTIGER_AERO_STYLE)

        self.history = [] # List to track scanned/generated items

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.setup_scan_tab()
        self.setup_generate_tab()
        self.setup_history_tab()
        
        self.paste_shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        self.paste_shortcut.activated.connect(self.handle_paste)

    def setup_scan_tab(self):
        scan_tab = QWidget()
        scan_layout = QVBoxLayout(scan_tab)

        self.drop_label = DropLabel()
        self.drop_label.main_app = self
        scan_layout.addWidget(self.drop_label, stretch=2)

        btn_layout = QHBoxLayout()
        self.btn_load_file = QPushButton("📂 Load File")
        self.btn_load_file.clicked.connect(self.load_file_dialog)
        
        self.btn_paste = QPushButton("📋 Paste Clipboard")
        self.btn_paste.clicked.connect(self.handle_paste)

        self.btn_screen_capture = QPushButton("🎥 Capture Screen")
        self.btn_screen_capture.clicked.connect(self.capture_screen)

        btn_layout.addWidget(self.btn_load_file)
        btn_layout.addWidget(self.btn_paste)
        btn_layout.addWidget(self.btn_screen_capture)
        scan_layout.addLayout(btn_layout)

        scan_layout.addWidget(QLabel("<b>🔮 Extracted Content:</b>"))
        self.scan_result_text = QTextEdit()
        self.scan_result_text.setReadOnly(True)
        scan_layout.addWidget(self.scan_result_text, stretch=1)

        self.tabs.addTab(scan_tab, "🔍 Scan QR")

    def setup_generate_tab(self):
        gen_tab = QWidget()
        gen_layout = QVBoxLayout(gen_tab)

        input_layout = QHBoxLayout()
        self.gen_input = QLineEdit()
        self.gen_input.setPlaceholderText("Enter text or URL to generate QR code...")
        
        self.btn_generate = QPushButton("✨ Generate")
        self.btn_generate.clicked.connect(self.generate_qr)
        
        input_layout.addWidget(self.gen_input)
        input_layout.addWidget(self.btn_generate)
        gen_layout.addLayout(input_layout)

        color_layout = QHBoxLayout()
        self.fill_color = "black"
        self.back_color = "white"

        self.btn_fg_color = QPushButton("🎨 Set QR Color (Black)")
        self.btn_bg_color = QPushButton("🎨 Set BG Color (White)")
        self.btn_fg_color.clicked.connect(self.choose_fg_color)
        self.btn_bg_color.clicked.connect(self.choose_bg_color)

        color_layout.addWidget(self.btn_fg_color)
        color_layout.addWidget(self.btn_bg_color)
        gen_layout.addLayout(color_layout)

        self.qr_display = QLabel()
        self.qr_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_display.setStyleSheet("background-color: #FAFAFA; border: 2px dashed #a3dcff; border-radius: 12px;")
        gen_layout.addWidget(self.qr_display, stretch=1)

        self.btn_save_qr = QPushButton("💾 Save QR Code")
        self.btn_save_qr.clicked.connect(self.save_qr)
        self.btn_save_qr.setEnabled(False)
        gen_layout.addWidget(self.btn_save_qr)

        self.tabs.addTab(gen_tab, "✏️ Generate QR")
        self.current_generated_img = None

    def setup_history_tab(self):
        hist_tab = QWidget()
        hist_layout = QVBoxLayout(hist_tab)
        
        self.history_list = QListWidget()
        hist_layout.addWidget(QLabel("<b>📜 Activity History:</b>"))
        hist_layout.addWidget(self.history_list)

        self.btn_export_history = QPushButton("📄 Export History to txt")
        self.btn_export_history.clicked.connect(self.export_history)
        hist_layout.addWidget(self.btn_export_history)

        self.tabs.addTab(hist_tab, "📜 History")

    def add_history(self, action, text):
        entry = f"[{action}] {text}"
        self.history.append(entry)
        self.history_list.addItem(entry)

    def choose_fg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.fill_color = color.name()
            self.btn_fg_color.setText(f"🎨 Set QR Color ({self.fill_color})")

    def choose_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.back_color = color.name()
            self.btn_bg_color.setText(f"🎨 Set BG Color ({self.back_color})")

    def handle_paste(self):
        clipboard = QApplication.clipboard()
        mime_data = clipboard.mimeData()
        
        if mime_data.hasImage():
            image = clipboard.image()
            self.process_qimage(image)
        elif mime_data.hasUrls():
            urls = mime_data.urls()
            if urls:
                self.process_image_file(urls[0].toLocalFile())
        else:
            QMessageBox.information(self, "No Image", "There is no image in the clipboard.")

    def load_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_path:
            self.process_image_file(file_path)

    def capture_screen(self):
        self.hide() # Hide window briefly
        QTimer.singleShot(500, self.do_capture)

    def do_capture(self):
        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(0)
        self.show() # Show immediately
        
        qimage = pixmap.toImage()
        self.process_qimage(qimage)

    def process_image_file(self, file_path):
        try:
            pil_img = Image.open(file_path)
            self.decode_and_display(pil_img)
            pixmap = QPixmap(file_path).scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)
            self.drop_label.setPixmap(pixmap)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load image: {e}")

    def process_qimage(self, qimage: QImage):
        # Convert QImage to pure PIL Image properly handling formats
        pil_img = ImageQt.fromqimage(qimage)
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")
        self.decode_and_display(pil_img)
        
        pixmap = QPixmap.fromImage(qimage).scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)
        self.drop_label.setPixmap(pixmap)

    def decode_and_display(self, pil_img: Image.Image):
        self.tabs.setCurrentIndex(0) 
        results = QRProcessor.decode_qr(pil_img)
        
        if not results:
            self.scan_result_text.setText("🍃 No QR codes found in the image.")
            self.scan_result_text.setStyleSheet("color: #7b1fa2;")
            return

        self.scan_result_text.setStyleSheet("color: #005a96;")
        output = ""
        for i, text in enumerate(results):
            output += f"--- 🌟 QR Code {i+1} ---\n{text}\n\n"
            self.add_history("SCANNED", text)
            
            if i == 0 and QRProcessor.is_url(text):
                reply = QMessageBox.question(
                    self, 'URL Detected', 
                    f"A URL was detected:\n\n{text}\n\nDo you want to open it?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                    QMessageBox.StandardButton.Yes
                )
                if reply == QMessageBox.StandardButton.Yes:
                    webbrowser.open(text)

        self.scan_result_text.setText(output)

    def generate_qr(self):
        text = self.gen_input.text().strip()
        if not text:
            QMessageBox.warning(self, "Input Required", "Please enter some text or URL.")
            return

        pil_img = QRProcessor.generate_qr(text, fill_color=self.fill_color, back_color=self.back_color)
        self.current_generated_img = pil_img
        
        qimage = ImageQt.ImageQt(pil_img)
        pixmap = QPixmap.fromImage(qimage).scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)
        self.qr_display.setPixmap(pixmap)
        self.btn_save_qr.setEnabled(True)
        
        self.add_history("GENERATED", text)

    def save_qr(self):
        if not self.current_generated_img:
            return
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save QR Code", "qrcode.png", "PNG Image (*.png);;All Files (*)"
        )
        if file_path:
            self.current_generated_img.save(file_path)
            QMessageBox.information(self, "Success", f"QR code saved to {os.path.basename(file_path)}")

    def export_history(self):
        if not self.history:
            QMessageBox.information(self, "Empty", "No history to export.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export History", "qr_history.txt", "Text Files (*.txt);;All Files (*)"
        )
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                for item in self.history:
                    f.write(item + '\n')
            QMessageBox.information(self, "Success", "History exported successfully!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnyQRApp()
    window.show()
    sys.exit(app.exec())
