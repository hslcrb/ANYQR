import sys
import os
import io
import zipfile
import argparse
import json
import xml.etree.ElementTree as ET
from PIL import Image
from qr_processor import QRProcessor

LONG_HELP = """
AnyQR Advanced CLI - Version 1.7.2
==================================

Powerful QR code generation and scanning with full GUI/CLI parity.

USAGE:
  AnyQR.exe <Command> [Options]

COMMANDS:
  /help             Show this comprehensive help message.
  /scan <path>      Scan an image file for QR codes.
  /gen <text>       Generate a QR code for the given text.
  /batch <path>     Batch generate QR codes from a text file (one line per QR).
  /config <path>    Process an external JSON or XML configuration file.

OPTIONS:
  /output <path>    Define the output filename (PNG, SVG, or ZIP for batch).
  /fill <color>     QR foreground color (e.g., black, #FF0000, "blue").
  /back <color>     QR background color or 'transparent' (e.g., white, #FFFFFF00).
  /svg              Export as high-quality SVG vector instead of PNG.

EXAMPLES:
  1. Scan a file:
     AnyQR.exe /scan "./my_qr.png"

  2. Generate a custom QR:
     AnyQR.exe /gen "https://google.com" /output "google.png" /fill "blue" /back "#f0f0f0"

  3. Generate a transparent SVG:
     AnyQR.exe /gen "Secret data" /output "hidden.svg" /svg /back transparent

  4. Batch generation (outputs a ZIP file):
     AnyQR.exe /batch "./links.txt" /output "all_qrs.zip"

  5. External Automation (JSON):
     Run: AnyQR.exe /config "tasks.json"
     JSON format:
     {
       "commands": [
         {"action": "gen", "text": "Task1", "output": "1.png", "fill": "red"},
         {"action": "scan", "path": "1.png"}
       ]
     }

  6. External Automation (XML):
     Run: AnyQR.exe /config "tasks.xml"
     XML format:
     <anyqr>
       <command action="gen" text="TaskX" output="x.svg" svg="true" />
     </anyqr>

NOTES:
- The GUI launches automatically if no CLI arguments are provided.
- CLI output is standardized to English for better compatibility with logs and automation.
"""

def process_gen(text, output=None, fill="black", back="white", svg=False):
    out = output or ("qrcode.svg" if svg else "qrcode.png")
    if svg:
        svg_data = QRProcessor.generate_qr_svg(text)
        with open(out, 'w', encoding='utf-8') as f:
            f.write(svg_data)
    else:
        p_back = "transparent" if back.lower() == "transparent" else back
        pil_img = QRProcessor.generate_qr(text, fill_color=fill, back_color=p_back)
        pil_img.save(out)
    print(f"Generated QR for '{text}' -> {out}")

def process_scan(path):
    try:
        pil_img = Image.open(path)
        results = QRProcessor.decode_qr(pil_img)
        if results:
            for idx, text in enumerate(results):
                print(f"Detected [{idx+1}]: {text}")
        else:
            print(f"No QR found in {path}")
    except Exception as e:
        print(f"Scan failed: {e}")

def run_cli():
    # Use argparse with slash prefix support
    parser = argparse.ArgumentParser(description="AnyQR Advanced CLI", prefix_chars='/', add_help=False)
    parser.add_argument("/scan", help="Scan image: /scan <path>")
    parser.add_argument("/gen", help="Generate QR: /gen <text>")
    parser.add_argument("/output", help="Output path")
    parser.add_argument("/fill", default="black", help="Foreground color")
    parser.add_argument("/back", default="white", help="Background color")
    parser.add_argument("/svg", action="store_true", help="Generate SVG")
    parser.add_argument("/batch", help="Batch file path")
    parser.add_argument("/config", help="JSON/XML config file path")
    parser.add_argument("/help", action="store_true", help="Show this help")
    
    try:
        args, unknown = parser.parse_known_args()
    except SystemExit:
        print(LONG_HELP)
        return True

    if args.help:
        print(LONG_HELP)
        return True

    if args.scan:
        process_scan(args.scan)
        return True

    if args.gen:
        process_gen(args.gen, args.output, args.fill, args.back, args.svg)
        return True

    if args.batch:
        out = args.output or "batch.zip"
        try:
            with open(args.batch, 'r', encoding='utf-8') as f:
                lines = [l.strip() for l in f if l.strip()]
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as z:
                for idx, line in enumerate(lines):
                    p_back = "transparent" if args.back.lower() == "transparent" else args.back
                    pi = QRProcessor.generate_qr(line, fill_color=args.fill, back_color=p_back)
                    buf = io.BytesIO()
                    pi.save(buf, format='PNG')
                    z.writestr(f"qr_{idx+1}.png", buf.getvalue())
            with open(out, 'wb') as f: f.write(zip_buffer.getvalue())
            print(f"Batch done: {len(lines)} items -> {out}")
        except Exception as e: print(f"Batch failed: {e}")
        return True

    if args.config:
        path = args.config
        try:
            if path.endswith('.json'):
                with open(path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for cmd in data.get("commands", []):
                        action = cmd.get("action")
                        if action == "gen":
                            process_gen(cmd.get("text"), cmd.get("output"), cmd.get("fill", "black"), cmd.get("back", "white"), cmd.get("svg", False))
                        elif action == "scan":
                            process_scan(cmd.get("path"))
            elif path.endswith('.xml'):
                tree = ET.parse(path)
                root = tree.getroot()
                for cmd in root.findall('command'):
                    action = cmd.get('action')
                    if action == "gen":
                        process_gen(cmd.get('text'), cmd.get('output'), cmd.get('fill', "black"), cmd.get('back', "white"), cmd.get('svg', "false").lower() == "true")
                    elif action == "scan":
                        process_scan(cmd.get('path'))
            else:
                print("Unsupported config format. Use .json or .xml")
        except Exception as e:
            print(f"Config failed: {e}")
        return True
        
    return False
