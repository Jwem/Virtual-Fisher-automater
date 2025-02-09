# Fisher Automator

This script automates interactions for the Fisher game. It uses pixel color detection to determine when to adjust delay values and to verify captcha challenges.

## Features

- **Automated Commands:** Issues various commands (e.g., buying, selling, fishing) based on timers.
- **Pixel Color Detection:** Uses predefined pixel positions and colors to monitor game state.
- **Captcha Verification:** Automatically detects captchas and regenerates codes up to 5 times if verification fails.
- **Customizable Settings:** Modify pixel coordinates and expected colors; use the `PixelColorViewer.ps1` script to identify values that work for your setup.

## Setup

1. Ensure you have Python, [PyAutoGUI](https://pyautogui.readthedocs.io/), and Tesseract installed.
2. Update the pixel positions and colors in the script as needed.
3. Run the PowerShell script `PixelColorViewer.ps1` (found in this folder) to calibrate settings for your monitor.

## Notes

- **Monitor Variations:** The pixel positions and colors might be different on other monitors.
- **Captcha Loop:** The script includes a loop to regenerate captcha codes up to 5 times if verification fails.

## Usage

Run the script using:
```bash
python Automater.py
```

Press `ESC` at any time to exit the automation.