import pyautogui
import time
import keyboard
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

screenshot = pyautogui.screenshot(region=(407, 893, 140, 27))
result_text = pytesseract.image_to_string(screenshot)
print(result_text)

if "Incorrect" not in result_text:
    print("Verified with code: 1234")