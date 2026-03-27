FRUTIGER_AERO_STYLE = """
#CentralWidget {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #d4f0ff, stop: 1 #ffffff);
    border: 1px solid #005a96;
    border-radius: 10px;
}
QMainWindow { background: transparent; }
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
QLabel, QCheckBox {
    color: #1a4d80;
    font-size: 14px;
    font-weight: bold;
}
QDialog { background-color: #d4f0ff; }
#TitleBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 156, 241, 0.8), stop:1 rgba(0, 100, 200, 0.9));
    border-top-left-radius: 10px;
    border-top-right-radius: 10px;
    border-bottom: 2px solid #005a96;
}
#TitleLabel { color: white; font-weight: bold; font-size: 14px; }
#TitleButton { 
    background: transparent; 
    border-radius: 4px; 
    color: white; 
    font-weight: bold; 
    font-size: 14px; 
    min-width: 30px; 
    padding: 4px;
}
#TitleButton:hover { background-color: rgba(255, 255, 255, 0.2); }
#CloseButton:hover { background-color: #ff4d4d; }
"""

LIGHT_MINIMAL_STYLE = """
#CentralWidget { background-color: #f9f9f9; border: 1px solid #ccc; border-radius: 8px; }
QMainWindow { background: transparent; }
QTabWidget::pane { border: 1px solid #e0e0e0; background-color: white; border-radius: 8px; }
QTabBar::tab { background: transparent; padding: 10px 20px; color: #555; font-weight: 500;}
QTabBar::tab:selected { background: white; border-bottom: 2px solid #007aff; color: #007aff; font-weight: bold; }
QPushButton { background-color: #f0f0f0; border: 1px solid #ccc; border-radius: 6px; padding: 8px 16px; color: #333; font-weight: 500;}
QPushButton:hover { background-color: #e4e4e4; }
QLineEdit, QTextEdit, QListWidget, QComboBox { border: 1px solid #ccc; border-radius: 6px; padding: 6px; background-color: white; color: #333; }
QLabel, QCheckBox { color: #333; font-size: 14px; }
QDialog { background-color: #f9f9f9; }
#TitleBar { background-color: #f8f8f8; border-bottom: 1px solid #ccc; }
#TitleLabel { color: #333; font-weight: 500; font-size: 14px; }
#TitleButton { background: transparent; color: #333; border-radius: 4px; min-width: 30px; }
#TitleButton:hover { background-color: #ddd; }
"""

DARK_MINIMAL_STYLE = """
#CentralWidget { background-color: #1e1e1e; border: 1px solid #444; border-radius: 8px; }
QMainWindow { background: transparent; }
QTabWidget::pane { border: 1px solid #333; background-color: #252526; border-radius: 8px; }
QTabBar::tab { background: transparent; padding: 10px 20px; color: #ccc; font-weight: 500;}
QTabBar::tab:selected { background: #252526; border-bottom: 2px solid #007aff; color: #fff; font-weight: bold; }
QPushButton { background-color: #333; border: 1px solid #444; border-radius: 6px; padding: 8px 16px; color: #eee; font-weight: 500;}
QPushButton:hover { background-color: #444; }
QLineEdit, QTextEdit, QListWidget, QComboBox { border: 1px solid #444; border-radius: 6px; padding: 6px; background-color: #1e1e1e; color: #eee; }
QLabel, QCheckBox { color: #eee; font-size: 14px; }
QDialog { background-color: #1e1e1e; }
#TitleBar { background-color: #2d2d2d; border-bottom: 1px solid #444; }
#TitleLabel { color: #eee; font-weight: 500; font-size: 14px; }
#TitleButton { background: transparent; color: #eee; border-radius: 4px; min-width: 30px; }
#TitleButton:hover { background-color: #555; }
"""

FRUTIGER_AERO_DARK_STYLE = """
#CentralWidget {
    background: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 1, stop: 0 #001a33, stop: 1 #003366);
    border: 1px solid #004d80;
    border-radius: 10px;
}
QMainWindow { background: transparent; }
QTabWidget::pane {
    border: 1px solid #1a4d80;
    background: rgba(0, 26, 51, 0.7);
    border-radius: 12px;
}
QTabBar::tab {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #003366, stop: 1 #001a33);
    border: 1px solid #1a4d80;
    border-radius: 6px;
    padding: 10px 20px;
    margin-right: 4px;
    margin-bottom: -1px;
    color: #80c4ff;
    font-weight: bold;
}
QTabBar::tab:selected, QTabBar::tab:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #004d99, stop: 1 #002b80);
    color: #ffffff;
}
QPushButton {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #009cf1, stop: 0.5 #007bbd, stop: 0.51 #006da8, stop: 1 #007bbd);
    border: 1px solid #004d80;
    border-radius: 15px;
    padding: 10px 20px;
    color: white;
    font-size: 14px;
    font-weight: bold;
}
QPushButton:hover {
    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #27aff7, stop: 0.5 #0087d8, stop: 0.51 #007bbd, stop: 1 #0087d8);
}
QLineEdit, QTextEdit, QListWidget, QComboBox {
    border: 2px solid #1a4d80;
    border-radius: 8px;
    padding: 6px;
    background-color: rgba(0, 26, 51, 0.85);
    selection-background-color: #009cf1;
    color: #80c4ff;
}
QLabel, QCheckBox {
    color: #80c4ff;
    font-size: 14px;
    font-weight: bold;
}
QDialog { background-color: #001a33; }
#TitleBar {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 rgba(0, 31, 63, 0.9), stop:1 rgba(0, 15, 30, 1.0));
    border-bottom: 2px solid #003366;
}
#TitleLabel { color: #80c4ff; font-weight: bold; font-size: 14px; }
#TitleButton { 
    background: transparent; 
    border-radius: 4px; 
    color: #80c4ff; 
    font-weight: bold; 
    font-size: 14px; 
    min-width: 30px; 
    padding: 4px;
}
#TitleButton:hover { background-color: rgba(128, 196, 255, 0.2); }
#CloseButton:hover { background-color: #990000; color: white; }
"""

THEMES = {
    "Frutiger Aero": FRUTIGER_AERO_STYLE,
    "Frutiger Aero Dark": FRUTIGER_AERO_DARK_STYLE,
    "Light Minimal": LIGHT_MINIMAL_STYLE,
    "Dark Minimal": DARK_MINIMAL_STYLE
}
