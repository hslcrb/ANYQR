# AnyQR (애니큐알)

AnyQR is a versatile QR code super-app built in Python with PyQt6. It allows users to generate, scan, and extract contents from QR codes directly through image files or clipboard pasting.

## Features
- **Generate QR Codes**: Create high-quality QR codes from text or URLs.
- **Scan from Files**: Drag and drop an image file to extract QR code data.
- **Scan from Clipboard**: Simply copy an image and press `Ctrl+V` to scan instantly.
- **Automatic Link Extraction**: Instantly detects and offers to open URLs.

## Requirements
- Python 3.9+
- On Windows, `pyzbar` may require the Visual C++ Redistributable Package.

## Installation
```bash
pip install -r requirements.txt
```

## Usage
Run the main application interface:
```bash
cd src
python main.py
```
