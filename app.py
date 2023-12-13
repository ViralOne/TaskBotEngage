import re
import time
import random
import pyautogui
import pyperclip
from datetime import datetime

# Constants
DEBUG = True
LOG_FILE = 'completed_tasks.log'
TELEGRAM_GROUP_URL = "https://web.telegram.org/a/#-1001936563741"
TELEGRAM_BOT_URL = "https://web.telegram.org/a/#1987747444"
#real-bot 5632459916

# Vars
last_processed_task = None
like_btn_x, like_btn_y = 587, 754
grab_img_x, grab_img_y = 1162, 205
drop_img_x, drop_img_y = 639, 639

def get_telegram_message():
    if not DEBUG:
        time.sleep(5)
        print("Looking for a new task...")
        pyautogui.hotkey('ctrl', 't')  # Open a new tab
        time.sleep(1)
        pyautogui.typewrite(TELEGRAM_GROUP_URL)  # Open Telegram
        pyautogui.press('enter')
        time.sleep(5)

        pyautogui.click(750, 750)  # Click on the chat area
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'c')

        clipboard_content = pyperclip.paste()

        task_pattern = r"【Task (\d+)】"
        link_pattern = r"https?://\S+"
        task_matches = re.findall(task_pattern, clipboard_content)
        link_matches = re.findall(link_pattern, clipboard_content)

        if task_matches and link_matches:
            tasks_and_links = list(zip(task_matches, link_matches))
            latest_task_number, latest_link = max(tasks_and_links, key=lambda x: int(x[0]))
            return latest_task_number, latest_link
        else:
            print("No Task number or link found.")
            return None, None
    else:
        return "13", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

def copy_file_to_clipboard(file_path='screenshot.png'):
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
            pyperclip.copy(file_content)
        return True
    except FileNotFoundError:
        return False

def send_task(task_number ,url):
    presses_number = random.randint(2, 15)

    time.sleep(2)
    pyautogui.hotkey('ctrl', 't')
    pyautogui.typewrite(url)
    pyautogui.press('enter')
    time.sleep(10)
    pyautogui.press('space')
    pyautogui.press('l', presses=presses_number)
    time.sleep(1)
    pyautogui.click(like_btn_x, like_btn_y)  # Click Like
    time.sleep(3)
    
    # Define the initial values for screenshot
    x_start = 20
    y_start = 120
    width = 900
    height = 700

    # Generate random offsets
    x_offset = random.randint(-15, 15)
    y_offset = random.randint(-15, 15)
    width_offset = random.randint(-35, 35)
    height_offset = random.randint(-35, 35)
    
    # Calculate the new values with the offsets
    x_new = x_start + x_offset
    y_new = y_start + y_offset
    width_new = width + width_offset
    height_new = height + height_offset

    # Take screenshot
    pyautogui.screenshot(region=(x_new, y_new, width_new, height_new)).save(r'screenshot.png')
    time.sleep(1)
    pyautogui.click(like_btn_x, like_btn_y)  # Take Like back
    print("Sreenshot saved")
    time.sleep(2)
    # Close tabs and send proof
    pyautogui.hotkey('ctrl', 'w', presses_number='2')  # Close tabs
    time.sleep(1)
    pyautogui.hotkey('ctrl', 't')  # Open a new tab
    time.sleep(1)
    pyautogui.typewrite(TELEGRAM_BOT_URL)  # Open Telegram bot conversation
    pyautogui.press('enter')
    time.sleep(5)

    pyautogui.moveTo(grab_img_x, grab_img_y, duration=1)
    pyautogui.mouseDown()
    pyautogui.moveTo(drop_img_x, drop_img_y, duration=2)

    # Wait for a moment to ensure proper drag operation
    time.sleep(1)
    pyautogui.mouseUp()

    time.sleep(1)
    pyautogui.click(drop_img_x, drop_img_y)
    pyautogui.press('tab', presses=4)
    time.sleep(1)

    # Paste Task number
    pyperclip.copy("Task " + task_number)
    pyautogui.hotkey('ctrl', 'v')
    
    pyautogui.press('enter')
    print(f"Task {task_number} was sent")

def main():
    global last_processed_task
    
    task_number, task_url = get_telegram_message()

    if task_number and task_url:
        print(f"Found Task {task_number}: {task_url}")

        if task_number == last_processed_task:
            print(f"Same task number ({task_number}) found again. Waiting for the next task...")
            time.sleep(40 * 60)
        else:
            send_task(task_number, task_url)
            last_processed_task = task_number

            # Log completed task
            now = datetime.now()
            current_date_time = now.strftime("%Y-%m-%d %H:%M:%S")
            with open(LOG_FILE, 'a') as log:
                log.write(f"{current_date_time} - Task {task_number}: {task_url}\n")
    else:
        print("No Task information with YouTube URL found in Telegram messages.")

if __name__ == "__main__":
    while True:
        main()
        
        print("Waiting for 40 minutes before the next execution...")
        time.sleep(40 * 60)