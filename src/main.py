import sys
import os
import webbrowser
import io
import zipfile
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QLineEdit, QTabWidget, QTextEdit, 
                             QFileDialog, QMessageBox, QListWidget, QComboBox, QColorDialog,
                             QCheckBox)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPixmap, QImage, QKeySequence, QShortcut, QClipboard, QScreen, QIcon
from PIL import ImageQt, Image
from qr_processor import QRProcessor
from styles import THEMES
from translations import TRANSLATIONS

try:
    import pyi_splash
except ImportError:
    pyi_splash = None

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
        self.setup_ui()
        
        # Set Window Icon
        icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "statics", "icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # Close Splash Screen if present
        if pyi_splash:
            pyi_splash.close()

    @property
    def t(self):
        return TRANSLATIONS[self.lang]

    def setup_ui(self):
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
        self.setup_batch_tab()
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
        self.chk_transparent = QCheckBox()
        color_layout.addWidget(self.chk_transparent)
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

    def setup_batch_tab(self):
        batch_widget = QWidget()
        batch_layout = QVBoxLayout(batch_widget)
        
        self.lbl_batch_info = QLabel()
        self.lbl_batch_info.setWordWrap(True)
        batch_layout.addWidget(self.lbl_batch_info)
        
        self.batch_input = QTextEdit()
        batch_layout.addWidget(self.batch_input)
        
        self.btn_batch_generate = QPushButton()
        self.btn_batch_generate.clicked.connect(self.generate_batch_qr)
        batch_layout.addWidget(self.btn_batch_generate)
        
        self.tabs.addTab(batch_widget, "")

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
        self.tabs.setTabText(2, t["tab_batch"])
        self.tabs.setTabText(3, t["tab_hist"])
        self.tabs.setTabText(4, t["tab_settings"])

        self.drop_label.setText(t["drop_text"])
        self.btn_load_file.setText(t["btn_load_file"])
        self.btn_paste.setText(t["btn_paste"])
        self.btn_screen_capture.setText(t["btn_capture"])
        self.lbl_extracted.setText(t["lbl_extracted"])

        self.gen_input.setPlaceholderText(t["gen_placeholder"])
        self.btn_generate.setText(t["btn_gen"])
        self.btn_set_fg.setText(f'{t["btn_set_fg"]} ({self.fill_color})')
        self.btn_set_bg.setText(f'{t["btn_set_bg"]} ({self.back_color})')
        self.chk_transparent.setText(t["chk_transparent"])
        self.btn_save_qr.setText(t["btn_save_qr"])

        self.lbl_batch_info.setText(t["lbl_batch_info"])
        self.btn_batch_generate.setText(t["btn_batch_gen"])

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
        color = QColorDialog.getColor(
            initial=Qt.GlobalColor.black,
            options=QColorDialog.ColorDialogOption.ShowAlphaChannel
        )
        if color.isValid():
            self.fill_color = color.getRgb() # Returns (r, g, b, a)
            self.btn_set_fg.setText(f'{self.t["btn_set_fg"]} ({self.fill_color})')

    def choose_bg_color(self):
        color = QColorDialog.getColor(
            initial=Qt.GlobalColor.white,
            options=QColorDialog.ColorDialogOption.ShowAlphaChannel
        )
        if color.isValid():
            self.back_color = color.getRgb()
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

        back = "transparent" if self.chk_transparent.isChecked() else self.back_color
        pil_img = QRProcessor.generate_qr(text, fill_color=self.fill_color, back_color=back)
        self.current_generated_img = pil_img
        
        # PIL to QImage conversion for display (maintains alpha)
        qimage = ImageQt.ImageQt(pil_img)
        pixmap = QPixmap.fromImage(qimage).scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio)
        self.qr_display.setPixmap(pixmap)
        self.btn_save_qr.setEnabled(True)
        
        self.add_history("GENERATED", text)

    def save_qr(self):
        if not self.current_generated_img:
            return
        
        t = self.t
        t = self.t
        file_path, _ = QFileDialog.getSaveFileName(self, t["btn_save_qr"], "qrcode.png", "PNG Image (*.png);;SVG Vector (*.svg);;All Files (*)")
        if file_path:
            if file_path.lower().endswith('.svg'):
                svg_data = QRProcessor.generate_qr_svg(self.gen_input.text().strip())
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(svg_data)
            else:
                self.current_generated_img.save(file_path)
            QMessageBox.information(self, t["save_success_title"], t["save_success_msg"].format(file=os.path.basename(file_path)))

    def generate_batch_qr(self):
        t = self.t
        text_data = self.batch_input.toPlainText().strip()
        if not text_data:
            QMessageBox.warning(self, t["input_required_title"], t["batch_empty_msg"])
            return

        lines = [line.strip() for line in text_data.split('\n') if line.strip()]
        if not lines:
            QMessageBox.warning(self, t["input_required_title"], t["batch_empty_msg"])
            return

        file_path, _ = QFileDialog.getSaveFileName(self, t["btn_batch_gen"], "batch_qrcodes.zip", t["save_zip_filter"])
        if not file_path:
            return

        try:
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                for idx, line in enumerate(lines):
                    # For batch, we use current colors but maybe standard PNG for simplicity
                    back = "transparent" if self.chk_transparent.isChecked() else self.back_color
                    pil_img = QRProcessor.generate_qr(line, fill_color=self.fill_color, back_color=back)
                    
                    img_byte_arr = io.BytesIO()
                    pil_img.save(img_byte_arr, format='PNG')
                    zip_file.writestr(f"qr_{idx+1}.png", img_byte_arr.getvalue())
            
            with open(file_path, 'wb') as f:
                f.write(zip_buffer.getvalue())
            
            QMessageBox.information(self, t["save_success_title"], t["batch_success_msg"].format(count=len(lines), file=os.path.basename(file_path)))
            
            # Record in history
            for line in lines:
                self.add_history("BATCH", line)
                
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Batch generation failed: {str(e)}")

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
