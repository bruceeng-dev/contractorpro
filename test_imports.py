import os
print("1. Imported os")

os.environ['DISABLE_MODEL_SOURCE_CHECK'] = 'True'
print("2. Set environment variable")

import sys
print(f"3. Python: {sys.executable}")

import pytesseract
print("4. Imported pytesseract")

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
print("5. Configured tesseract path")

import cv2
print("6. Imported cv2")

import pandas as pd
print("7. Imported pandas")

print("8. All imports successful!")
print("9. Now testing video opening...")

VIDEO_PATH = r"C:\Users\RLESo\OneDrive - TPT\Documents\PokemonClassification\Pokémon Red⧸Blue ｜｜ Complete (100%) Walkthrough\PokemonRed_FullGameplay.mp4"
cap = cv2.VideoCapture(VIDEO_PATH)
if cap.isOpened():
    print("10. Video opened successfully!")
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"11. FPS: {fps}")
    cap.release()
else:
    print("10. ERROR: Could not open video")

print("12. Test complete!")
