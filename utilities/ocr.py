import logging
import pytesseract
from PIL import Image
from utils import print_log
from datetime import datetime as time

# Set logging to show only errors (suppress debug/info/warnings)
logging.basicConfig(level=logging.ERROR)

def perform_ocr(image_path):
    """
    Perform Optical Character Recognition (OCR) on the image located at image_path.
    The extracted text is saved into a text file named with the original image name,
    with '_output' appended before the file extension.

    Args:
    image_path (str): The path to the image file to be processed (assumed to be a PNG file).
    """
    start = time.now()
    img = Image.open(image_path)
    ocr_result = pytesseract.image_to_string(img)
    output_path = image_path.replace('/ss/', '/ocr/')
    output_path = output_path.replace('.png', '_ocr.txt')

    # Write the OCR results (text) into a new text file
    with open(output_path, 'w') as f:
        f.write(ocr_result.strip())
        
    end = time.now()
    print_log(f"OCR completed in {end - start} seconds. Saved to {output_path}")
