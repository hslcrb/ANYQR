import sys
import os
import webbrowser
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QTabWidget, QTextEdit, 
                             QFileDialog, QMessageBox, QListWidget, QComboBox, QColorDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage, QKeySequence, QShortcut, QClipboard, QScreen
from PIL import ImageQt, Image
from qr_processor import QRProcessor
from styles import THEMES
from translations import TRANSLATIONS

class DropLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
        self.lang = "ko"
        self.current_theme = "Frutiger Aero"
        self.history = []

        self.resize(850, 650)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.setup_scan_tab()
        self.setup_generate_tab()
        self.setup_history_tab()
        self.setup_settings_tab()
        
        self.paste_shortcut = QShortcut(QKeySequence("Ctrl+V"), self)
        self.paste_shortcut.activated.connect(self.handle_paste)

        self.apply_theme()
        self.update_texts()

    @property
    def t(self):
        return TRANSLATIONS[self.lang]

    def setup_scan_tab(self):
        scan_tab = QWidget()
        scan_layout = QVBoxLayout(scan_tab)

        self.drop_label = DropLabel()
        self.drop_label.main_app = self
        scan_layout.addWidget(self.drop_label, stretch=2)

        btn_layout = QHBoxLayout()
        self.btn_load_file = QPushButton()
        self.btn_load_file.clicked.connect(self.load_file_dialog)
        
        self.btn_paste = QPushButton()
        self.btn_paste.clicked.connect(self.handle_paste)

        self.btn_screen_capture = QPushButton()
        self.btn_screen_capture.clicked.connect(self.capture_screen)

        btn_layout.addWidget(self.btn_load_file)
        btn_layout.addWidget(self.btn_paste)
        btn_layout.addWidget(self.btn_screen_capture)
        scan_layout.addLayout(btn_layout)

        self.lbl_extracted = QLabel()
        scan_layout.addWidget(self.lbl_extracted)
        self.scan_result_text = QTextEdit()
        self.scan_result_text.setReadOnly(True)
        scan_layout.addWidget(self.scan_result_text, stretch=1)

        self.tabs.addTab(scan_tab, "")

    def setup_generate_tab(self):
        gen_tab = QWidget()
        gen_layout = QVBoxLayout(gen_tab)

        input_layout = QHBoxLayout()
        self.gen_input = QLineEdit()
        
        self.btn_generate = QPushButton()
        self.btn_generate.clicked.connect(self.generate_qr)
        
        input_layout.addWidget(self.gen_input)
        input_layout.addWidget(self.btn_generate)
        gen_layout.addLayout(input_layout)

        color_layout = QHBoxLayout()
        self.fill_color = "black"
        self.back_color = "white"

        self.btn_set_fg = QPushButton()
        self.btn_set_bg = QPushButton()
        self.btn_set_fg.clicked.connect(self.choose_fg_color)
        self.btn_set_bg.clicked.connect(self.choose_bg_color)

        color_layout.addWidget(self.btn_set_fg)
        color_layout.addWidget(self.btn_set_bg)
        gen_layout.addLayout(color_layout)

        self.qr_display = QLabel()
        self.qr_display.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.qr_display.setStyleSheet("background-color: transparent; border: 2px dashed #a3dcff; border-radius: 12px;")
        gen_layout.addWidget(self.qr_display, stretch=1)

        self.btn_save_qr = QPushButton()
        self.btn_save_qr.clicked.connect(self.save_qr)
        self.btn_save_qr.setEnabled(False)
        gen_layout.addWidget(self.btn_save_qr)

        self.tabs.addTab(gen_tab, "")
        self.current_generated_img = None

    def setup_history_tab(self):
        hist_tab = QWidget()
        hist_layout = QVBoxLayout(hist_tab)
        
        self.history_list = QListWidget()
        self.lbl_history = QLabel()
        hist_layout.addWidget(self.lbl_history)
        hist_layout.addWidget(self.history_list)

        self.btn_export_history = QPushButton()
        self.btn_export_history.clicked.connect(self.export_history)
        hist_layout.addWidget(self.btn_export_history)

        self.tabs.addTab(hist_tab, "")

    def setup_settings_tab(self):
        set_tab = QWidget()
        set_layout = QVBoxLayout(set_tab)

        self.lbl_settings = QLabel()
        set_layout.addWidget(self.lbl_settings)

        # Language selection
        lang_layout = QHBoxLayout()
        self.lbl_lang = QLabel()
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(["한국어 (ko)", "English (en)"])
        self.combo_lang.currentIndexChanged.connect(self.change_language)
        lang_layout.addWidget(self.lbl_lang)
        lang_layout.addWidget(self.combo_lang)
        lang_layout.addStretch()

        # Theme selection
        theme_layout = QHBoxLayout()
        self.lbl_theme = QLabel()
        self.combo_theme = QComboBox()
        self.combo_theme.addItems(["Frutiger Aero", "Frutiger Aero Dark", "Light Minimal", "Dark Minimal"])
        self.combo_theme.currentIndexChanged.connect(self.change_theme)
        theme_layout.addWidget(self.lbl_theme)
        theme_layout.addWidget(self.combo_theme)
        theme_layout.addStretch()

        set_layout.addLayout(lang_layout)
        set_layout.addLayout(theme_layout)
        set_layout.addStretch()

        self.tabs.addTab(set_tab, "")

    def change_language(self, index):
        if index == 0:
            self.lang = "ko"
        else:
            self.lang = "en"
        self.update_texts()

    def change_theme(self, index):
        self.current_theme = self.combo_theme.currentText()
        self.apply_theme()

    def apply_theme(self):
        style = THEMES.get(self.current_theme, THEMES["Frutiger Aero"])
        self.setStyleSheet(style)
        
        # Adjust specific drop label colors based on theme if needed
        if "Dark" in self.current_theme:
            if "Frutiger" in self.current_theme:
                self.drop_label.setStyleSheet("border: 2px dashed #009cf1; border-radius: 15px; background-color: rgba(0, 26, 51, 0.6); color: #80c4ff; font-size: 18px; padding: 20px;")
                self.qr_display.setStyleSheet("background-color: transparent; border: 2px dashed #1a4d80; border-radius: 12px;")
            else:
                self.drop_label.setStyleSheet("border: 2px dashed #555; border-radius: 15px; color: #aaa; font-size: 18px; padding: 20px;")
                self.qr_display.setStyleSheet("background-color: transparent; border: 2px dashed #555; border-radius: 12px;")
        elif "Light" in self.current_theme:
            self.drop_label.setStyleSheet("border: 2px dashed #ccc; border-radius: 15px; color: #555; font-size: 18px; padding: 20px;")
            self.qr_display.setStyleSheet("background-color: transparent; border: 2px dashed #ccc; border-radius: 12px;")
        else:
            self.drop_label.setStyleSheet("border: 2px dashed #009cf1; border-radius: 15px; background-color: rgba(255, 255, 255, 0.6); color: #005a96; font-size: 18px; padding: 20px;")
            self.qr_display.setStyleSheet("background-color: transparent; border: 2px dashed #a3dcff; border-radius: 12px;")

    def update_texts(self):
        t = self.t
        self.setWindowTitle(t["app_title"])
        self.tabs.setTabText(0, t["tab_scan"])
        self.tabs.setTabText(1, t["tab_gen"])
        self.tabs.setTabText(2, t["tab_hist"])
        self.tabs.setTabText(3, t["tab_settings"])

        self.drop_label.setText(t["drop_text"])
        self.btn_load_file.setText(t["btn_load_file"])
        self.btn_paste.setText(t["btn_paste"])
        self.btn_screen_capture.setText(t["btn_capture"])
        self.lbl_extracted.setText(t["lbl_extracted"])

        self.gen_input.setPlaceholderText(t["gen_placeholder"])
        self.btn_generate.setText(t["btn_gen"])
        self.btn_set_fg.setText(f'{t["btn_set_fg"]} ({self.fill_color})')
        self.btn_set_bg.setText(f'{t["btn_set_bg"]} ({self.back_color})')
        self.btn_save_qr.setText(t["btn_save_qr"])

        self.lbl_history.setText(t["lbl_history"])
        self.btn_export_history.setText(t["btn_export_hist"])

        self.lbl_settings.setText(t["lbl_settings"])
        self.lbl_lang.setText(t["lbl_language"])
        self.lbl_theme.setText(t["lbl_theme"])

    def add_history(self, action, text):
        entry = f"[{action}] {text}"
        self.history.append(entry)
        self.history_list.addItem(entry)

    def choose_fg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.fill_color = color.name()
            self.btn_set_fg.setText(f'{self.t["btn_set_fg"]} ({self.fill_color})')

    def choose_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.back_color = color.name()
            self.btn_set_bg.setText(f'{self.t["btn_set_bg"]} ({self.back_color})')

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
            QMessageBox.information(self, self.t["no_image_title"], self.t["no_image_msg"])

    def load_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if file_path:
            self.process_image_file(file_path)

    def capture_screen(self):
        self.hide()
        QTimer.singleShot(500, self.do_capture)

    def do_capture(self):
        screen = QApplication.primaryScreen()
        pixmap = screen.grabWindow(0)
        self.show()
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
        pil_img = ImageQt.fromqimage(qimage)
        if pil_img.mode != "RGB":
            pil_img = pil_img.convert("RGB")
        self.decode_and_display(pil_img)
        
        pixmap = QPixmap.fromImage(qimage).scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)
        self.drop_label.setPixmap(pixmap)

    def decode_and_display(self, pil_img: Image.Image):
        self.tabs.setCurrentIndex(0) 
        results = QRProcessor.decode_qr(pil_img)
        
        t = self.t
        if not results:
            self.scan_result_text.setText(t["no_qr_found"])
            if "Dark" in self.current_theme:
                self.scan_result_text.setStyleSheet("color: #ffaaaa;")
            else:
                self.scan_result_text.setStyleSheet("color: #d32f2f;")
            return

        if "Dark" in self.current_theme:
            self.scan_result_text.setStyleSheet("color: #aaddff;")
        else:
            self.scan_result_text.setStyleSheet("color: #005a96;")
            
        output = ""
        for i, text in enumerate(results):
            output += t["qr_detected"].format(num=i+1, text=text)
            self.add_history("SCANNED", text)
            
            if i == 0 and QRProcessor.is_url(text):
                reply = QMessageBox.question(
                    self, t["url_detected_title"], 
                    t["url_detected_msg"].format(text=text),
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
                    QMessageBox.StandardButton.Yes
                )
                if reply == QMessageBox.StandardButton.Yes:
                    webbrowser.open(text)

        self.scan_result_text.setText(output)

    def generate_qr(self):
        text = self.gen_input.text().strip()
        t = self.t
        if not text:
            QMessageBox.warning(self, t["input_required_title"], t["input_required_msg"])
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
        
        t = self.t
        file_path, _ = QFileDialog.getSaveFileName(self, t["btn_save_qr"], "qrcode.png", "PNG Image (*.png);;All Files (*)")
        if file_path:
            self.current_generated_img.save(file_path)
            QMessageBox.information(self, t["save_success_title"], t["save_success_msg"].format(file=os.path.basename(file_path)))

    def export_history(self):
        t = self.t
        if not self.history:
            QMessageBox.information(self, t["empty_hist_title"], t["empty_hist_msg"])
            return

        file_path, _ = QFileDialog.getSaveFileName(self, t["btn_export_hist"], "qr_history.txt", "Text Files (*.txt);;All Files (*)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as f:
                for item in self.history:
                    f.write(item + '\n')
            QMessageBox.information(self, t["export_success_title"], t["export_success_msg"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AnyQRApp()
    window.show()
    sys.exit(app.exec())
