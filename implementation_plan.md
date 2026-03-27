# AnyQR (애니큐알) Implementation Plan

## Goal Description
AnyQR is a comprehensive "Super App" for QR codes built in Python. The application will allow users to generate, scan, and manage QR codes effortlessly. A key feature is the ability to instantly scan QR codes by pasting images directly from the clipboard or dragging and dropping image files. Immediate extraction and handling of links/text will be supported. 

## User Review Required
> [!IMPORTANT]
> The application will be built using **PyQt6** for a modern graphical user interface and **pyzbar** + **Pillow** for QR code detection. Please confirm if these libraries are acceptable, or if you prefer an alternative framework like Tkinter or PySide6.

## Proposed Changes

### Core Project Structure
The project will be structured systematically in `d:\anyqr`:

#### [NEW] [README.md](file:///d:/anyqr/README.md)
Project overview and instructions.

#### [NEW] [requirements.txt](file:///d:/anyqr/requirements.txt)
Python dependencies (`PyQt6`, `qrcode`, `pyzbar`, `Pillow`, `opencv-python`).

### Source Code (`src/`)

#### [NEW] [main.py](file:///d:/anyqr/src/main.py)
The entry point of the PyQt6 application.

#### [NEW] [ui.py](file:///d:/anyqr/src/ui.py)
Handles the GUI layout, including the clipboard paste event (`Ctrl+V`), drag-and-drop areas, and result displays.

#### [NEW] [qr_processor.py](file:///d:/anyqr/src/qr_processor.py)
Contains the core logic for:
1. Generating QR codes from user input text.
2. Decoding QR codes using `pyzbar` from raw image bytes, Pillow Images, or OpenCV formats.
3. Automatically detecting URLs and offering actions.

## Phase 15: Professional Polish (Icon, Splash, Batch)
- **Application Icon**: Use `statics/icon.ico` for both the window icon and the executable icon.
- **Splash Screen**: Display the icon as a splash screen during application cold start.
- **Batch Generation**: A new sub-feature allowing users to generate multiple QR codes at once from a list of inputs.
- **Optimization**: Modularize code where necessary and improve UI responsiveness.

## Verification Plan

### Manual Verification
- **Splash Test**: Run the compiled `.exe` and verify the icon appears as a splash screen first.
- **Icon Test**: Verify the taskbar and window top-left corner show the `icon.ico`.
- **Batch Test**: Input multiple lines (e.g., 3 different URLs) and verify multiple QR images are generated/zip-exported.
- **Save/Export**: Verify all options (PNG, SVG) work correctly in the new features.
