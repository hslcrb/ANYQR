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
QLineEdit, QTextEdit, QListWidget, QComboBox {
    border: 2px solid #a3dcff;
    border-radius: 8px;
    padding: 6px;
    background-color: rgba(255, 255, 255, 0.85);
    selection-background-color: #009cf1;
    color: #333;
}
QLabel {
    color: #1a4d80;
    font-size: 14px;
    font-weight: bold;
}
"""

LIGHT_MINIMAL_STYLE = """
QMainWindow { background-color: #f9f9f9; }
QTabWidget::pane { border: 1px solid #e0e0e0; background-color: white; border-radius: 8px; }
QTabBar::tab { background: transparent; padding: 10px 20px; color: #555; font-weight: 500;}
QTabBar::tab:selected { background: white; border-bottom: 2px solid #007aff; color: #007aff; font-weight: bold; }
QPushButton { background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 6px; padding: 8px 16px; color: #333; font-weight: 500;}
QPushButton:hover { background-color: #e4e4e4; }
QLineEdit, QTextEdit, QListWidget, QComboBox { border: 1px solid #ccc; border-radius: 6px; padding: 6px; background-color: white; color: #333; }
QLabel { color: #333; font-size: 14px; }
"""

DARK_MINIMAL_STYLE = """
QMainWindow { background-color: #1e1e1e; }
QTabWidget::pane { border: 1px solid #333; background-color: #252526; border-radius: 8px; }
QTabBar::tab { background: transparent; padding: 10px 20px; color: #ccc; font-weight: 500;}
QTabBar::tab:selected { background: #252526; border-bottom: 2px solid #007aff; color: #fff; font-weight: bold; }
QPushButton { background-color: #333; border: 1px solid #444; border-radius: 6px; padding: 8px 16px; color: #eee; font-weight: 500;}
QPushButton:hover { background-color: #444; }
QLineEdit, QTextEdit, QListWidget, QComboBox { border: 1px solid #444; border-radius: 6px; padding: 6px; background-color: #1e1e1e; color: #eee; }
QLabel { color: #eee; font-size: 14px; }
"""

THEMES = {
    "Frutiger Aero": FRUTIGER_AERO_STYLE,
    "Light Minimal": LIGHT_MINIMAL_STYLE,
    "Dark Minimal": DARK_MINIMAL_STYLE
}
