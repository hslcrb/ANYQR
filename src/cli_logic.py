import sys
import os
import io
import zipfile
import argparse
import json
import xml.etree.ElementTree as ET
from PIL import Image
from qr_processor import QRProcessor

# CLI State
current_lang = "en"

CLI_TRANSLATIONS = {
    "en": {
        "welcome": "\nAnyQR Advanced CLI - Version 1.7.4\n[NOTICE] You can switch language using '/lang ko' | 언어 전환을 위해 '/lang ko'를 입력하세요.\nType '/help' for a full command list or '/exit' to quit.",
        "prompt": "AnyQR ({lang})> ",
        "lang_switched": "Language switched to English.",
        "invalid_lang": "Invalid language. Use 'en' or 'ko'.",
        "exit_msg": "Goodbye!",
        "unknown_cmd": "Unknown command. Type /help for assistance.",
        "scan_fail": "Scan failed: {e}",
        "no_qr": "No QR found in {path}",
        "gen_success": "Generated QR for '{text}' -> {out}",
        "batch_success": "Batch done: {count} items -> {out}",
        "batch_fail": "Batch failed: {e}",
        "config_fail": "Config failed: {e}",
        "config_unsupported": "Unsupported config format. Use .json or .xml",
    },
    "ko": {
        "welcome": "\n애니큐알(AnyQR) 고급 CLI - 버전 1.7.4\n[안내] '/lang en'을 입력하여 언어를 변경할 수 있습니다. | Type '/lang en' to switch to English.\n전체 명령어 목록은 '/help'를, 종료는 '/exit'를 입력하세요.",
        "prompt": "애니큐알 ({lang})> ",
        "lang_switched": "언어가 한국어로 변경되었습니다.",
        "invalid_lang": "잘못된 언어입니다. 'en' 또는 'ko'를 입력하세요.",
        "exit_msg": "안녕히 가세요!",
        "unknown_cmd": "알 수 없는 명령어입니다. 도움이 필요하면 /help를 입력하세요.",
        "scan_fail": "스캔 실패: {e}",
        "no_qr": "{path}에서 QR 코드를 찾을 수 없습니다.",
        "gen_success": "'{text}'에 대한 QR 생성 완료 -> {out}",
        "batch_success": "배정 작업 완료: {count}개 항목 -> {out}",
        "batch_fail": "배치 작업 실패: {e}",
        "config_fail": "구성 파일 처리 실패: {e}",
        "config_unsupported": "지원되지 않는 형식입니다. .json 또는 .xml을 사용하세요.",
    }
}

def get_help():
    if current_lang == "ko":
        return """
애니큐알(AnyQR) 고급 CLI 도움말
==============================

사용법:
  AnyQR.exe <명령어> [옵션]

명령어:
  /help             이 도움말 메시지를 표시합니다.
  /lang <en|ko>     CLI 언어를 변경합니다.
  /scan <경로>      이미지 파일에서 QR 코드를 스캔합니다.
  /gen <내용>       입력한 텍스트로 QR 코드를 생성합니다.
  /batch <경로>     텍스트 파일에서 한 줄 한 항목씩 대량 생성합니다.
  /config <경로>    외부 JSON 또는 XML 설정 파일을 처리합니다.
  /exit, /quit      프로그램을 종료합니다 (대화형 모드 전용).

옵션:
  /output <경로>    출력 파일명 정의 (PNG, SVG, 또는 ZIP).
  /fill <색상>      QR 전경색 (예: black, #FF0000, "blue").
  /back <색상>      QR 배경색 또는 'transparent' (예: white, #00000000).
  /svg              PNG 대신 고품질 SVG 벡터로 저장합니다.

예시:
  1. 스캔: AnyQR.exe /scan "./my_qr.png"
  2. 생성: AnyQR.exe /gen "안녕하세요" /output "hi.png" /fill "blue"
  3. 설정 파일 자동화: AnyQR.exe /config "tasks.json"
"""
    else:
        return """
AnyQR Advanced CLI Help
=======================

USAGE:
  AnyQR.exe <Command> [Options]

COMMANDS:
  /help             Show this comprehensive help message.
  /lang <en|ko>     Switch CLI language.
  /scan <path>      Scan an image file for QR codes.
  /gen <text>       Generate a QR code for the given text.
  /batch <path>     Batch generate QR codes from a text file (one line per QR).
  /config <path>    Process an external JSON or XML configuration file.
  /exit, /quit      Close the application (Interactive mode only).

OPTIONS:
  /output <path>    Define the output filename (PNG, SVG, or ZIP for batch).
  /fill <color>     QR foreground color (e.g., black, #FF0000, "blue").
  /back <color>     QR background color or 'transparent' (e.g., white, #FFFFFF00).
  /svg              Export as high-quality SVG vector instead of PNG.

EXAMPLES:
  1. Scan a file: AnyQR.exe /scan "./my_qr.png"
  2. Custom QR: AnyQR.exe /gen "Hello" /output "hi.png" /fill "blue"
  3. Automation: AnyQR.exe /config "tasks.json"
"""

def process_gen(text, output=None, fill="black", back="white", svg=False):
    t = CLI_TRANSLATIONS[current_lang]
    out = output or ("qrcode.svg" if svg else "qrcode.png")
    try:
        if svg:
            svg_data = QRProcessor.generate_qr_svg(text)
            with open(out, 'w', encoding='utf-8') as f:
                f.write(svg_data)
        else:
            p_back = "transparent" if back.lower() == "transparent" else back
            pil_img = QRProcessor.generate_qr(text, fill_color=fill, back_color=p_back)
            pil_img.save(out)
        print(t["gen_success"].format(text=text, out=out))
    except Exception as e:
        print(f"Error: {e}")

def process_scan(path):
    t = CLI_TRANSLATIONS[current_lang]
    try:
        pil_img = Image.open(path)
        results = QRProcessor.decode_qr(pil_img)
        if results:
            for idx, text in enumerate(results):
                print(f"Detected [{idx+1}]: {text}")
        else:
            print(t["no_qr"].format(path=path))
    except Exception as e:
        print(t["scan_fail"].format(e=e))

def run_cli(args_list=None):
    global current_lang
    t = CLI_TRANSLATIONS[current_lang]
    
    parser = argparse.ArgumentParser(description="AnyQR Advanced CLI", prefix_chars='/', add_help=False)
    parser.add_argument("/scan", help="Scan image")
    parser.add_argument("/gen", help="Generate QR")
    parser.add_argument("/output", help="Output path")
    parser.add_argument("/fill", default="black", help="Foreground color")
    parser.add_argument("/back", default="white", help="Background color")
    parser.add_argument("/svg", action="store_true", help="Generate SVG")
    parser.add_argument("/batch", help="Batch file path")
    parser.add_argument("/config", help="Config file path")
    parser.add_argument("/lang", help="Switch language")
    parser.add_argument("/help", action="store_true", help="Show help")
    parser.add_argument("/exit", action="store_true")
    parser.add_argument("/quit", action="store_true")
    
    try:
        if args_list is None:
            args, unknown = parser.parse_known_args()
        else:
            args, unknown = parser.parse_known_args(args_list)
    except SystemExit:
        print(get_help())
        return True

    if args.help:
        print(get_help())
        return True
    
    if args.exit or args.quit:
        return "EXIT"

    if args.lang:
        if args.lang.lower() in ["en", "ko"]:
            current_lang = args.lang.lower()
            print(CLI_TRANSLATIONS[current_lang]["lang_switched"])
        else:
            print(t["invalid_lang"])
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
            print(t["batch_success"].format(count=len(lines), out=out))
        except Exception as e: print(t["batch_fail"].format(e=e))
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
                print(t["config_unsupported"])
        except Exception as e:
            print(t["config_fail"].format(e=e))
        return True
        
    return False

def interactive_shell():
    print(CLI_TRANSLATIONS[current_lang]["welcome"])
    while True:
        try:
            prompt = CLI_TRANSLATIONS[current_lang]["prompt"].format(lang=current_lang)
            user_input = input(prompt).strip()
            if not user_input:
                continue
            
            # Simple split by whitespace, but better would be shlex for quotes.
            # However, for our slash commands, space separation is usually enough.
            import shlex
            try:
                cmd_args = shlex.split(user_input)
            except ValueError:
                cmd_args = user_input.split()
                
            res = run_cli(cmd_args)
            if res == "EXIT":
                print(CLI_TRANSLATIONS[current_lang]["exit_msg"])
                break
            elif res is False:
                print(CLI_TRANSLATIONS[current_lang]["unknown_cmd"])
        except (EOFError, KeyboardInterrupt):
            print("\n" + CLI_TRANSLATIONS[current_lang]["exit_msg"])
            break
        except Exception as e:
            print(f"Error: {e}")
