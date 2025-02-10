import pyautogui
import time
import keyboard
from PIL import Image
import pytesseract
import threading

# Specify the path to the Tesseract executable if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Initialize global variables
delay = 2.7
antiBotActive = False
buying = False
boat = False
stop_script = False
last_command_time = time.time()
last_click_time = time.time()
last_boost_time = time.time()
last_upgrade_time = time.time()
last_daily_time = time.time()

def check_pixel_color_private_msg():
    x, y = 1500, 880
    expected_color = (52, 53, 65)
    pixel_color = pyautogui.pixel(x, y)
    return pixel_color == expected_color

def text_captcha():
    region = (300, 600, 700, 350)  
    screenshot = pyautogui.screenshot(region=region)
    text = pytesseract.image_to_string(screenshot)
    return text

def image_captcha():
    region = (315, 837, 505, 48)  
    screenshot = pyautogui.screenshot(region=region)
    text = pytesseract.image_to_string(screenshot)
    return text

def upgrade_boat():
    global boat  # add this line to use the global variable
    global last_click_time
    boat = True
    coordinates = [(642, 925), (500, 915), (650, 883), (500, 925)]
    for x, y in coordinates:
        pyautogui.click(x, y)
        time.sleep(2)
    last_click_time = time.time()

def check_balance():
    region = (310, 750, 374, 153)
    screenshot = pyautogui.screenshot(region=region)
    text = pytesseract.image_to_string(screenshot)
    if "You now have $" in text:
        balance = text.split("You now have")[1].split("!")[0]
        return balance
    else:
        return "Balance not found"

def buying_boosts():
    global buying
    global last_boost_time
    buying = True
    print("Buying boosts...")
    commands = [
        '/buy Auto10m',
        '/buy Fish5m',
        '/buy Treasure5m',
        '/buy Auto30m',
        '/buy Fish20m',
        '/buy Treasure20m',
        '/buy Fish Ovens',
    ]
    for command in commands:
        if check_anti_bot_and_verify():
            print("Anti-bot verification failed during buying boosts. Exiting...")
            return
        pyautogui.write(command)
        pyautogui.press('enter')
        pyautogui.press('enter')
        time.sleep(3)
    last_boost_time = time.time()

def buying_upgrades():
    global buying
    global last_upgrade_time
    buying = True
    print("Buying upgrades...")
    upgrades = [
        '/buy Better Fish',
        '/buy Salesman',
        '/buy Bait Efficiency',
        '/buy More Chests',
        '/buy Worker Motivation',
        '/buy Better Fish',
        '/buy Artifact Specialist',
        '/buy Experienced',
        '/buy Better Chests',
        '/buy Better Dailies',
    ]
    for upgrade in upgrades:
        if check_anti_bot_and_verify():
            print("Anti-bot verification failed during buying upgrades. Exiting...")
            return
        pyautogui.write(upgrade)
        pyautogui.press('enter')
        pyautogui.press('enter')
        time.sleep(3)
    last_upgrade_time = time.time()

def remote_turn_off():
    text = text_captcha()
    if "Remote" in text:
        return True

def check_anti_bot_and_verify():
    global antiBotActive
    text = text_captcha()  # assign text variable
    if "Anti-bot" in text:
        antiBotActive = True
        print("Anti-bot detected.")
        # Check for "Code:" once using a regional screenshot
        text = text_captcha()
        if "Code:" in text:
            start_index = text.find("Code:") + len("Code:")
            remainder = text[start_index:].strip()
            code = remainder.split()[0] if remainder.split() else ""
            # Remove non-alphanumeric characters
            code = ''.join(e for e in code if e.isalnum())
            if code:
                pyautogui.write(f"/verify")
                time.sleep(0.2)  # Wait for the command to be typed
                pyautogui.write(" " + code)
                time.sleep(0.2)  # Wait for the code to be typed
                pyautogui.press('enter')
                result_text = text_captcha()
                time.sleep(5)  # Wait for verification to complete

                if "Incorrect" not in result_text:
                    print(f"Verified with code: {code}")
                    antiBotActive = False
                    return False  # Continue normal operation
                
                print(f"Verification failed with code: {code}")
                print("Falling back to image captcha...")

        # Fallback to image captcha if "Code:" is absent
        img_text = image_captcha()
        img_text = ''.join(e for e in img_text if e.isalnum())
        pyautogui.write(f"/verify")
        time.sleep(0.2)  # Wait for the command to be typed
        pyautogui.write(" " + img_text)
        pyautogui.press('enter')
        time.sleep(3)
        screenshot = pyautogui.screenshot(region=(407, 893, 140, 27))
        result_text = pytesseract.image_to_string(screenshot)
        if "Incorrect" not in result_text:
            print(f"Verified with image code: {img_text}") 
            antiBotActive = False
            return False  # Continue normal operation
        
        # Regen loop: try up to 5 times
        regen_attempt = 0
        while regen_attempt < 5:
            pyautogui.write("/verify regen")
            time.sleep(0.2)
            pyautogui.press('enter')
            print(f"Regeneration attempt {regen_attempt+1}")
            time.sleep(3)
            # First, check using regional text extraction for "Code:"
            regenerated_text = text_captcha()
            if "Code:" in regenerated_text:
                start_index = regenerated_text.find("Code:") + len("Code:")
                remainder = regenerated_text[start_index:].strip()
                code = remainder.split()[0] if remainder.split() else ""
                # Remove non-alphanumeric characters
                code = ''.join(e for e in code if e.isalnum())
                if code:
                    pyautogui.write(f"/verify")
                    time.sleep(0.2)
                    pyautogui.write(" " + code)
                    pyautogui.press('enter')
                    time.sleep(3)
                    screenshot = pyautogui.screenshot(region=(407, 893, 140, 27))
                    result_text = pytesseract.image_to_string(screenshot)
                    if "Incorrect" not in result_text:
                        print(f"Verified with new code: {code}")
                        antiBotActive = False
                        return False  # Continue normal operation
            else:
                # Fallback to image captcha if "Code:" is absent
                img_text = image_captcha()
                img_text = ''.join(e for e in img_text if e.isalnum())
                pyautogui.write(f"/verify")
                time.sleep(0.2)
                pyautogui.write(" " + img_text)
                pyautogui.press('enter')
                time.sleep(3)
                screenshot = pyautogui.screenshot(region=(407, 893, 140, 27))
                result_text = pytesseract.image_to_string(screenshot)
                if "Incorrect" not in result_text:
                    print(f"Verified with image code: {img_text}")
                    antiBotActive = False
                    return False  # Continue normal operation
            regen_attempt += 1
        print("Verification unsuccessful after 5 regens. Exiting...")
        antiBotActive = False
        return True  # Stop the main loop
    return False

def listen_for_esc():
    global stop_script
    keyboard.wait('esc')
    print("Escape key pressed. Exiting...")
    stop_script = True

def main():
    global delay, antiBotActive, buying, boat, stop_script, last_command_time, last_boost_time, last_upgrade_time, last_daily_time
    print("2 seconds to move to the desired window.")
    time.sleep(2)

    last_command_time = time.time()
    last_click_time = time.time()
    last_reduce_time = time.time()  # new timer for delay reduction

    try:
        while not stop_script:
            current_time = time.time()
            
            # New anti-bot check at each loop iteration
            if check_anti_bot_and_verify():
                print("Anti-bot verification failed. Exiting...")
                stop_script = True

            # Check for remote turn-off message
            if remote_turn_off():
                print("Remote turn-off message detected. Exiting...")
                stop_script = True

            # Skip issuing commands if anti-bot check is active
            if antiBotActive:
                continue
            
            if buying:
                time.sleep(15)
                buying = False

            if boat:
                time.sleep(5)
                boat = False

            if current_time - last_reduce_time >= 120:  # Every 2 minutes
                delay -= 0.1
                print(f"Reduced delay: {delay}")
                last_reduce_time = current_time

            if current_time - last_click_time >= 3600: # Every 1 hour
                upgrade_boat()
                last_click_time = current_time
            
            if current_time - last_boost_time >= 300:# Every 5 minutes
                buying_boosts()

            if current_time - last_upgrade_time >= 1800: # Every 30 minutes
                buying_upgrades()

            if current_time - last_daily_time >= 86400: # Every 24 hours
                pyautogui.write('/daily')
                pyautogui.press('enter')
                pyautogui.press('enter')
                last_daily_time = current_time

            if check_pixel_color_private_msg():
                print("Pixel color matched. Increasing delay...")
                delay += 0.1
                print(f"New delay: {delay}")
                            
            if current_time - last_command_time >= 600: # Every 10 minutes
                pyautogui.write('/sell all')
                pyautogui.press('enter')
                pyautogui.press('enter')
                time.sleep(1.5)
                last_command_time = current_time
                balance = check_balance()
                print(f"Balance: {balance}")

            else:
                pyautogui.write('/fish')
                pyautogui.press('enter')
                pyautogui.press('enter')
                time.sleep(delay)
    except KeyboardInterrupt:
        print("Program interrupted by user.")

if __name__ == "__main__":
    esc_listener = threading.Thread(target=listen_for_esc)
    esc_listener.start()
    main()
    esc_listener.join()