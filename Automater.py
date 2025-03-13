import pyautogui
import time
import keyboard
from PIL import Image
import pytesseract
import threading
import random

# Specify the path to the Tesseract executable if it's not in your PATH
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

has_supporter_rod = False
delay = 2.9
fishingx = 440
fishingy = 907
antiBotActive = False
buying = False
boat = False
stop_script = False
current_time = time.time()
balance = 0
level = 0
owned_rods = set()  # Keep track of owned rods
current_biome = "River"
ROD_ORDER = [
    "Improved Rod",     # 500
    "Steel Rod",        # 8,000 8K
    "Fiberglass Rod",   # 50,000 50K
    "Heavy Rod",        # 100,000 100K
    "Alloy Rod",        # 250,000 250K
    "Lava Rod",         # 1,000,000 1M
    "Magma Rod",        # 10,000,000 10M
    "Oceanium Rod",     # 75,000,000 75M 
    "Golden Rod",       # 120,000,000 120M
    "Superium Rod",     # 250,000,000 250M
    "Infinity Rod",     # 1,000,000,000 1B
    "Floating Rod",     # 50,000,000,000 50B
    "Sky Rod",          # 250,000,000,000 250B
    "Meteor Rod",       # 500,000,000,000 500B
    "Space Rod",        # 1,000,000,000,000 1T
    "Alien Rod"         # Price unknown
]
owned_boats = set()  # Keep track of owned boats
BOAT_ORDER = [
    "Rowboat",           # 2,500 2.5K
    "Fishing Boat",      # 25,000 25K
    "Speedboat",         # 100,000 100K
    "Pontoon",           # 250,000 250K
    "Sailboat",          # 1,000,000 1M
    "Yacht",             # 20,000,000 20M
    "Luxury Yacht",      # 100,000,000 100M
    "Cruise Ship",       # 500,000,000 500M
    "Goldboat",          # 2,500,000,000 2.5B
    "Sky cruiser",       # 10,000,000,000 10B
    "Satellite",         # 50,000,000,000 50B
    "Space Shuttle",     # 250,000,000,000 250B
    "Cruiser",           # 1,000,000,000,000 1T
    "Alien raft",        # 2,500,000,000,000 2.5T
    "Alien submarine"    # 5,000,000,000,000 5T
]

BIOMES = {
    0: ("River", "/biome River"),      # Starting biome
    50: ("Volcanic", "/biome Volcanic"), # Level 50
    100: ("Ocean", "/biome Ocean"),     # Level 100
    250: ("Sky", "/biome Sky"),         # Level 250
    500: ("Space", "/biome Space"),     # Level 500
    1000: ("Alien", "/biome Alien")      # Level 1000
}

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def initialize_prestige():
    global prestige
    print("What prestige level are you?") # Answer is an integer, save it
    prestige = int(input("> "))


def initialize_biome():
    global current_biome, new_biome, level
    
    print("\nWhich biome are you currently in?")
    for level_req, (biome_name, _) in sorted(BIOMES.items()):
        print(f"{biome_name} (Level {level_req})")
    
    while True:
        choice = input("> ").strip().title()
        for req_level, (biome_name, _) in BIOMES.items():
            if choice == biome_name:
                current_biome = choice
                new_biome = choice
                # Set the level to match the biome's requirement
                level = req_level
                log_message(f"Starting in biome: {current_biome} (Level {level})")
                return
        print("Invalid biome. Please choose from the list above.")


def initialize_owned_items(item_type):
    """Initialize owned items (rods or boats) through user input
    Args:
        item_type (str): Type of items to initialize ('rods' or 'boats')
    """
    global owned_rods, owned_boats, has_supporter_rod
    
    items = {
        'rods': [
            "Improved Rod",
            "Steel Rod",
            "Fiberglass Rod", 
            "Heavy Rod",
            "Alloy Rod",
            "Lava Rod",
            "Magma Rod",
            "Oceanium Rod",
            "Golden Rod",
            "Superium Rod",
            "Infinity Rod",
            "Floating Rod",
            "Sky Rod",
            "Meteor Rod",
            "Space Rod",
            "Alien Rod"
        ],
        'boats': [ 
            "Rowboat",
            "Fishing Boat",
            "Speedboat",
            "Pontoon",
            "Sailboat",
            "Yacht",
            "Luxury Yacht",
            "Cruise Ship",
            "Goldboat",
            "Sky cruiser",
            "Satellite",
            "Space Shuttle",
            "Cruiser",
            "Alien raft",
            "Alien submarine",
        ]
    }
    
    selected_items = items.get(item_type, [])
    if not selected_items:
        log_message(f"Invalid item type: {item_type}")
        return

    if item_type == 'rods':
        print("\nDo you have a supporter rod? (y/n)")
        supporter_choice = input("> ").strip().lower()
        has_supporter_rod = supporter_choice == 'y'
        if has_supporter_rod:
            log_message("Supporter rod detected - will skip certain rod upgrades")
    
    print(f"\nAvailable {item_type}:")
    for i in range(0, len(selected_items), 2):
        item1 = f"{i+1}. {selected_items[i]}"
        item2 = f"{i+2}. {selected_items[i+1]}" if i+1 < len(selected_items) else ""
        print(f"{item1:<30} {item2}")
    
    print(f"\nEnter the number of your highest tier {item_type[:-1]} (1-{len(selected_items)}), Plastic Rod not included.")
    print("All lower tier items will be automatically included.")
    print("Press Enter if you own none.")
    

    
    try:
        choice = input("> ").strip()
        owned_set = owned_rods if item_type == 'rods' else owned_boats
        
        if choice:
            index = int(choice) - 1
            if 0 <= index < len(selected_items):
                # Add the selected item and all items before it
                for i in range(index + 1):
                    owned_set.add(selected_items[i])
        
        if owned_set:
            log_message(f"Initialized with {item_type}: {', '.join(sorted(owned_set))}")
        else:
            log_message(f"Starting with no {item_type}")
    except ValueError:
        log_message("Invalid input, asking again...")
        initialize_owned_items(item_type)

def check_pixel_color_private_msg():
    x, y = 1500, 850
    expected_color = (46, 48, 53)
    expected_color_2 = (49, 51, 56)
    pixel_color = pyautogui.pixel(x, y)
    return pixel_color != expected_color and pixel_color != expected_color_2

def text_captcha():
    region = (300, 600, 700, 350)
    screenshot = pyautogui.screenshot(region=region)
    text = pytesseract.image_to_string(screenshot)
    return text

def image_captcha():
    region = (395, 880, 285, 50) # (left, top, width, height)
    screenshot = pyautogui.screenshot(region=region)
    text = pytesseract.image_to_string(screenshot)
    return text

def remote_turn_off():
    text = text_captcha()
    if "Remote" in text:
        log_message("Application closed by remote command.")
        pyautogui.write('Application closed by remote command.')
        pyautogui.press('enter')
        return True
    
def buying_boosts():
    global buying
    if buying:
        log_message("Buying boosts...")
        pyautogui.click(fishingx + 150, fishingy)
        time.sleep(1.5 + random.uniform(0, 1))
        pyautogui.click(fishingx + 50, fishingy)
        time.sleep(1.5 + random.uniform(0, 1))
        pyautogui.click(fishingx + 50, fishingy - 20)
        time.sleep(1.5 + random.uniform(0, 1))
        pyautogui.click(fishingx + 50, fishingy - 20)
        time.sleep(1.5 + random.uniform(0, 1))
        pyautogui.click(fishingx + 200, fishingy - 20)
        time.sleep(1.5 + random.uniform(0, 1))
        pyautogui.click(fishingx + 300, fishingy - 20)
        time.sleep(1.5 + random.uniform(0, 1))
        pyautogui.click(fishingx + 50, fishingy - 50)
        time.sleep(1.5 + random.uniform(0, 1))
        pyautogui.click(fishingx + 200, fishingy - 50)
        time.sleep(1.5 + random.uniform(0, 1))
        pyautogui.click(fishingx + 300, fishingy - 50)
        time.sleep(1.5 + random.uniform(0, 1))
        pyautogui.click(fishingx, fishingy)
        time.sleep(1.5 + random.uniform(0, 1))
        pyautogui.click(fishingx, fishingy)
        time.sleep(1.5 + random.uniform(0, 1))
        pyautogui.click(fishingx, fishingy)
        buying = False

def check_balance():
    global balance
    text = text_captcha()
    if "You now have $" in text:
        start_index = text.find("You now have $") + len("You now have $")
        remainder = text[start_index:].strip()
        string_balance = remainder.split()[0] if remainder.split() else ""
        # Remove any non-numeric characters except commas
        string_balance = ''.join(c for c in string_balance if c.isdigit() or c == ',')
        string_balance = string_balance.replace(",", "")
        try:
            balance = int(string_balance)
            return balance
        except ValueError:
            log_message(f"Error converting balance: {string_balance}")
    return None

def buy_rod():
    global balance, owned_rods, has_supporter_rod, level, prestige

    skip_rods = {
        "Improved Rod",
        "Steel Rod", 
        "Fiberglass Rod",
        "Lava Rod",
        "Magma Rod",
        "Oceanium Rod",
        "Sky Rod"
    }
    
    if prestige > 4:
        skip_rods.add("Alloy Rod")
    if prestige > 12:
        skip_rods.add("Superium Rod")
    if prestige > 30:
        skip_rods.add("Space Rod")
    if prestige > 85:
        skip_rods.add("Sky Rod")
        skip_rods.add("Space Rod")

    # Rod prices, commands, and required levels
    rods = {
        # Basic rods
        500: ("Improved Rod", "/buy Improved Rod", 0),
        8000: ("Steel Rod", "/buy Steel Rod", 0), 
        50000: ("Fiberglass Rod", "/buy Fiberglass Rod", 0),
        100000: ("Heavy Rod", "/buy Heavy Rod", 0),
        250000: ("Alloy Rod", "/buy Alloy Rod", 0),
        1000000: ("Lava Rod", "/buy Lava Rod", 0),
        10000000: ("Magma Rod", "/buy Magma Rod", 0),
        # Level 100 rods
        75000000: ("Oceanium Rod", "/buy Oceanium Rod", 100),
        120000000: ("Golden Rod", "/buy Golden Rod", 100),
        250000000: ("Superium Rod", "/buy Superium Rod", 100),
        1000000000: ("Infinity Rod", "/buy Infinity Rod", 100),
        # Level 250 rods
        50000000000: ("Floating Rod", "/buy Floating Rod", 250),
        250000000000: ("Sky Rod", "/buy Sky Rod", 250),
        # Level 500 rods
        500000000000: ("Meteor Rod", "/buy Meteor Rod", 500),
        1000000000000: ("Space Rod", "/buy Space Rod", 500),
    }
    
    affordable_rod = None
    affordable_price = 0
    
    for price, (rod_name, command, required_level) in sorted(rods.items()):
        if rod_name == "Heavy Rod" or rod_name == "Golden Rod" or rod_name == "Meteor Rod":
            continue
        if has_supporter_rod and rod_name in skip_rods:
            continue
        if balance >= price and rod_name not in owned_rods and level >= required_level:
            affordable_rod = command
            affordable_price = price
            rod_to_add = rod_name
            
    if affordable_rod:
        log_message(f"Buying new rod: {rod_to_add}")
        if anti_bot():
            return False
        pyautogui.write(affordable_rod)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')
        balance -= affordable_price
        owned_rods.add(rod_to_add)
        log_message(f"Owned rods: {', '.join(sorted(owned_rods, key=lambda x: ROD_ORDER.index(x)))}")
        time.sleep(1)
        if anti_bot():
            return False
        pyautogui.write('/fish')
        time.sleep(0.5)
        pyautogui.press('enter')
        pyautogui.press('enter')
        return True
    return False

def buy_boat():
    global balance, owned_boats, level
    # Boat prices, commands, and required levels
    boats = {
        # Basic boats
        2500: ("Rowboat", "/buy Rowboat", 0), # 2.5K
        25000: ("Fishing Boat", "/buy Fishing Boat", 0), # 25K
        100000: ("Speedboat", "/buy Speedboat", 0), # 100K
        250000: ("Pontoon", "/buy Pontoon", 0), # 250K
        1000000: ("Sailboat", "/buy Sailboat", 0), # 1M
        20000000: ("Yacht", "/buy Yacht", 0), # 20M
        # Level 50 boats
        100000000: ("Luxury Yacht", "/buy Luxury Yacht", 50), # 100M
        # Level 100 boats
        500000000: ("Cruise Ship", "/buy Cruise Ship", 100), # 500M
        # Level 250 boats
        2500000000: ("Goldboat", "/buy Goldboat", 250), # 2.5B
        10000000000: ("Sky cruiser", "/buy Sky cruiser", 250), # 10B
        # Level 500 boats
        50000000000: ("Satellite", "/buy Satellite", 500), # 50B
        250000000000: ("Space Shuttle", "/buy Space Shuttle", 500), # 250B
        1000000000000: ("Cruiser", "/buy Cruiser", 500), # 1T
        # Level 1000 boats
        2500000000000: ("Alien raft", "/buy Alien raft", 1000), # 2.5T
        5000000000000: ("Alien submarine", "/buy Alien submarine", 1000) # 5T
    }
    
    affordable_boat = None
    affordable_price = 0
    
    for price, (boat_name, command, required_level) in sorted(boats.items()):
        if balance >= price and boat_name not in owned_boats and level >= required_level:
            affordable_boat = command
            affordable_price = price
            boat_to_add = boat_name
            
    if affordable_boat:
        log_message(f"Buying new boat: {boat_to_add}")
        if anti_bot():
            return False
        pyautogui.write(affordable_boat)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.press('enter')
        balance -= affordable_price
        owned_boats.add(boat_to_add)
        log_message(f"Owned boats: {', '.join(sorted(owned_boats, key=lambda x: BOAT_ORDER.index(x)))}")
        time.sleep(1)
        if anti_bot():
            return False
        pyautogui.write('/fish')
        time.sleep(0.5)
        pyautogui.press('enter')
        pyautogui.press('enter')
        return True
    return False

def anti_bot():
    global antiBotActive
    text = text_captcha()  # assign text variable
    canRegen = True
    if "Anti-bot" in text:
        antiBotActive = True
        log_message("Anti-bot detected.")
        antiBotRanDelay = random.uniform(12, 25) # Random delay between 14 and 128 seconds
        time.sleep(antiBotRanDelay)
        
        regen_attempt = 0
        while canRegen:
            # Check for "Code:" using a regional screenshot
            text = text_captcha()
            if "Code:" in text:
                start_index = text.find("Code:") + len("Code:")
                remainder = text[start_index:].strip()
                code = remainder.split()[0] if remainder.split() else ""
                # Remove non-alphanumeric characters
                code = ''.join(e for e in code if e.isalnum())
                if code:
                    pyautogui.write(f"/verify {code}")
                    pyautogui.press('enter')
                    time.sleep(10)
                    result_text = text_captcha()
                    if "incorrect" not in result_text.lower():
                        log_message(f"Verified with code: {code}")
                        antiBotActive = False
                        pyautogui.write('/fish')
                        time.sleep(0.5)
                        pyautogui.press('enter')
                        pyautogui.press('enter')
                        time.sleep(2)
                        return False  # Continue normal operation
                    if "you have regenerated your captcha too many times" in result_text.lower():
                        log_message("Verification unsuccessful after 5 regens. Waiting for cooldown...")
                        pyautogui.write('Waiting for regen cooldown...')
                        pyautogui.press('enter')
                        time.sleep(900) # 15 minutes
                    log_message(f"Code: {code} failed. Regenerating...")
            else:
                # Fallback to image captcha if "Code:" is absent
                text = text_captcha()
                if 'captcha.' in text:
                    captcha = text.split('captcha.')[1].split('All')[0].replace('\n', '').replace(' ', '')
                    pyautogui.write(f"/verify {captcha}")
                    pyautogui.press('enter')
                    time.sleep(10)
                    result_text = text_captcha().lower()
                    if "incorrect" not in result_text.lower():
                        log_message(f"Verified with image code: {captcha}")
                        antiBotActive = False
                        pyautogui.write('/fish')
                        time.sleep(0.5)
                        pyautogui.press('enter')
                        pyautogui.press('enter')
                        time.sleep(2)
                        return False  # Continue normal operation
                    if "you have regenerated your captcha too many times" in result_text.lower():
                        log_message("Verification unsuccessful after 5 regens. Waiting for cooldown...")
                        pyautogui.write('Waiting for regen cooldown...')
                        pyautogui.press('enter')
                        time.sleep(900) # 15 minutes
                    log_message(f"Image code: {captcha} failed. Regenerating...")
            
            pyautogui.write("/verify regen")
            pyautogui.press('enter')
            log_message(f"Regeneration attempt {regen_attempt + 1}")
            time.sleep(3)
            regen_attempt += 1
        
        log_message("Verification unsuccessful after 5 regens. Exiting...")
        antiBotActive = False
        return True  # Stop the main loop
    return False

def listen_for_esc():
    global stop_script
    keyboard.wait('esc')
    log_message("Escape key pressed. Exiting...")
    stop_script = True

def log_message(message):
    timestamp = time.strftime('%H:%M:%S')
    print(f"[{timestamp}] {message}")

def main():
    sell_clicks = 0
    time_boosts = 0
    run_time = 0
    level = 0
    global delay, antiBotActive, buying, boat, stop_script, fishingx, fishingy, balance, owned_rods, owned_boats, has_supporter_rod, new_biome, current_biome
    log_message("2 seconds to move to the desired window.")
    time.sleep(2)


    last_reduce_time = time.time()  # new timer for delay reduction

    try:
        while not stop_script:
            time.sleep(random.uniform(0, 0.5))
            current_time = time.time()
            text = text_captcha().lower()
            # Random pauses to simulate human behavior

            if "this interaction failed" in text:
                time.sleep(20 + random.uniform(0, 10))

            if random.random() < 0.002:
                log_message("Random pause...")
                pause = random.uniform(5, 12)
                pyautogui.write(f'Random pause... {round((pause), 1)}s')
                pyautogui.press('enter')
                time.sleep(pause)
                if check_pixel_color_private_msg():
                    pyautogui.click(fishingx, fishingy - 200)
                    time.sleep(delay)
                else:
                    pyautogui.click(fishingx, fishingy - 65)
                    time.sleep(delay)
                time_boosts += pause
            if random.random() < 0.0037:
                log_message("Long random pause...")
                pause = random.uniform(33, 97)
                pyautogui.write(f'Long random pause... {round((pause), 1)}s')
                pyautogui.press('enter')
                time.sleep(pause)
                if check_pixel_color_private_msg():
                    pyautogui.click(fishingx, fishingy - 200)
                    time.sleep(delay)
                else:
                    pyautogui.click(fishingx, fishingy - 65)
                    time.sleep(delay)
                time_boosts += pause
            
            # The delay shouldn't realistically go that low or high so we exit the program
            if delay < 1 or delay > 6:
                log_message("Something is off with the delay... Exiting...")
                pyautogui.write('Something is off with the delay... Exiting...')
                pyautogui.press('enter')
                stop_script = True

            # New anti-bot check at each loop iteration
            if anti_bot():
                log_message("Anti-bot verification failed. Exiting...")
                pyautogui.write('Anti-bot verification failed. Exiting...')
                pyautogui.press('enter')
                stop_script = True

            # Check for remote turn-off message
            if remote_turn_off():
                log_message("Remote turn-off message detected. Exiting...")
                pyautogui.write('Remote turn-off message detected. Exiting...')
                pyautogui.press('enter')
                stop_script = True

            # Skip issuing commands if anti-bot check is active
            if antiBotActive:
                continue

            if current_time - last_reduce_time >= 300:  # every 5 minutes
                delay -= 0.1
                log_message(f"Reduced delay: {round((delay), 1)}")
                last_reduce_time = current_time

            if 'ended!' in text or 'stopped working' in text or time_boosts >= 1800:  # When boosts end or after 30 minutes
                run_time += time_boosts
                buying = True
                buying_boosts()
                time_boosts = 0

            if 'you can now prestige' in text:
                log_message("Prestiging...")
                pyautogui.write('/prestige reset')
                time.sleep(0.5)
                pyautogui.press('enter')
                pyautogui.press('enter')
                time.sleep(2)
                # Reset balance and owned items
                balance = 0
                owned_rods.clear()
                owned_boats.clear()
                current_biome = "River"
                new_biome = current_biome
                level = 0
                time.sleep(2)
                pyautogui.write('/fish')
                time.sleep(1)
                pyautogui.press('enter')
                pyautogui.press('enter')
                
            if 'you are now level' in text:
                try:
                    # More robust level extraction
                    level_text = text[text.find('you are now level'):].split('.')[0]
                    level_number = ''.join(filter(str.isdigit, level_text))
                    if level_number and int(level_number) < 15000:  # Limit to level 15,000
                        temp_level = int(level_number)
                        if temp_level > level:
                            level = temp_level

                    if current_biome == "Alien": # Skip biome change if in Alien biome
                        continue
                    # Check if we can even change biomes
                    highest_accessible_biome = current_biome
                    highest_level_req = 0
                    highest_biome_command = None

                    for level_req, (biome_name, biome_command) in sorted(BIOMES.items()):
                        if level >= level_req:
                            highest_accessible_biome = biome_name
                            highest_level_req = level_req
                            highest_biome_command = biome_command
                    
                    if highest_accessible_biome != current_biome and level <= 15000: # Limit to level 15,000
                        log_message(f"New biome: {highest_accessible_biome} (Level {level})")
                        current_biome = highest_accessible_biome
                        pyautogui.write(highest_biome_command)
                        pyautogui.press('enter')  # Also added this line to execute the command
                        pyautogui.write('/rod supporter')
                        pyautogui.press('enter')
                        time.sleep(0.5)
                        pyautogui.write('/fish')
                        time.sleep(0.5)
                        pyautogui.press('enter')
                        pyautogui.press('enter')

                except (IndexError, ValueError) as e:
                    log_message(f"Error parsing level: {e}")
                    log_message(f"Debug - Problematic text: {text}")

            if check_pixel_color_private_msg():
                pause = random.uniform(0, 6)
                time.sleep(pause)
                pyautogui.click(fishingx, fishingy - 115)
                delay += 0.1
                time_boosts += pause
                time.sleep(delay + random.uniform(0, 0.3))
                log_message(f"Pixel color matched. Increased delay: {round((delay), 1)}")

            if sell_clicks >= 10 + round(random.uniform(0, 5)):  # every 10-15 clicks
                pyautogui.click(fishingx + 100, fishingy)
                time.sleep(delay + random.uniform(0, 0.5))
                temp_balance = check_balance()
                if temp_balance is not None:
                    if temp_balance - 1 % 10 != 0:
                        balance = temp_balance # Only when last digit is 1 because the program sometimes mistakes exclamation marks for 1s
                        if balance:  # Only proceed if we got a valid balance
                            if buy_rod():  # Only try to buy boat if rod purchase failed
                                pass
                            else:
                                buy_boat()  # Try to buy boat only if we didn't buy a rod
                    sell_clicks = 0
            else:
                delay
                if random.random() < 0.1:
                    time.sleep(random.uniform(0, 1))
                else:
                    pyautogui.click(fishingx, fishingy)
                    time.sleep(delay)

                sell_clicks += 1
                time_boosts += delay

    except KeyboardInterrupt:
        log_message("Program interrupted by user.")

if __name__ == "__main__":
    initialize_owned_items('rods')
    initialize_owned_items('boats')
    initialize_biome()
    esc_listener = threading.Thread(target=listen_for_esc)
    esc_listener.start()
    main()
    esc_listener.join()