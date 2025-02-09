# Fisher Automator

This script automates interactions for the Fisher game. It uses pixel color detection and OCR for captcha verification.

## Features

- **Automated Commands:** Issues various commands (e.g., buying, selling, fishing) based on timers.
- **Pixel Color Detection:** Uses predefined pixel positions and colors to monitor game state.
- **Captcha Verification:** Automatically detects captchas and regenerates codes up to 5 times if verification fails.
- **Customizable Settings:** Modify pixel coordinates and expected colors; use the `PixelColorViewer.ps1` script to identify values that work for your setup.

## Installation

1. **Python Libraries:**
   - Install required Python libraries using:
     ```bash
     pip install pyautogui pillow pytesseract keyboard
     ```
2. **Tesseract OCR:**
   - Download and install Tesseract OCR from [here](https://github.com/tesseract-ocr/tesseract).
   - Update the `pytesseract.pytesseract.tesseract_cmd` variable in `Automater.py` with the correct path to the Tesseract executable.

## Setup

1. Ensure you have Python, [PyAutoGUI](https://pyautogui.readthedocs.io/), and Tesseract installed.
2. Update the pixel positions and colors in the script as needed.
3. Run the PowerShell script `PixelColorViewer.ps1` (found in this folder) to calibrate settings for your monitor.

## Usage

### Run Pixel Color Viewer
- Use the `PixelColorViewer.ps1` PowerShell script to identify pixel positions and RGB values on your monitor.
- Open PowerShell and run:
  ```powershell
  .\PixelColorViewer.ps1
  ```
- Move your cursor to the desired position and note the pixel coordinates and color.

### Update Script Configuration
- Open `Automater.py` and update the pixel positions/colors in the `check_pixel_color_private_msg` function and other relevant sections using the values obtained from the pixel color viewer.

### Run the Automator Script
- Open a terminal or command prompt in the project directory.
- Run the following command:
  ```bash
  python Automater.py
  ```
- Press the `Esc` key at any time to stop the script.

## Configuration

- **Delay Adjustment:** Modify the `delay` variable in the `main` function to adjust the interval between actions.
- **Anti-bot Verification:** The script uses OCR to extract and verify captcha codes. Ensure that the Tesseract OCR path is correctly set.
- **Pixel Settings:** Monitor variations may require you to update the pixel positions and color values based on your setup.

## Notes

- The pixel positions and colors might be different on other monitors. Use `PixelColorViewer.ps1` to obtain the correct values.
- The script includes a loop to regenerate captcha codes up to 5 times if verification fails.