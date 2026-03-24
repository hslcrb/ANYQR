import io
from PIL import Image
import qrcode
import cv2
import numpy as np
import re

class QRProcessor:
    @staticmethod
    def generate_qr(data: str, size: int = 10, border: int = 4, fill_color: str = "black", back_color: str = "white") -> Image.Image:
        """Generates a QR code image from the provided text/URL."""
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=size,
            border=border,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color=fill_color, back_color=back_color)
        # Ensure it's in a standard format (RGB) for GUI compatibility
        return img.convert("RGB")

    @staticmethod
    def decode_qr(image: Image.Image) -> list[str]:
        """Scans the image for QR codes and returns a list of decoded strings."""
        try:
            # Convert PIL image to OpenCV format (BGR)
            open_cv_image = np.array(image.convert('RGB'))
            open_cv_image = open_cv_image[:, :, ::-1].copy()
            
            # Use OpenCV's built-in QR Code detector
            detector = cv2.QRCodeDetector()
            retval, decoded_info, points, _ = detector.detectAndDecodeMulti(open_cv_image)
            
            results = []
            if retval:
                for text in decoded_info:
                    if text: # Sometimes it returns empty strings for partial matches
                        results.append(text)
            return results
        except Exception as e:
            print(f"Error decoding QR: {e}")
            return []

    @staticmethod
    def is_url(text: str) -> bool:
        """Checks if the decoded text is a URL."""
        url_pattern = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return re.match(url_pattern, text) is not None
