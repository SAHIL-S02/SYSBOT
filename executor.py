import pyautogui
import time
import os
import subprocess

pyautogui.FAILSAFE = True

# ---- CONFIG ----
BASE_CODE_DIR = r"D:\App File\Code"

VSCODE_PATH = os.path.expandvars(
    r"%LOCALAPPDATA%\Programs\Microsoft VS Code\Code.exe"
)

# ---- HELPERS ----
def ensure_folder(path):
    if not path.startswith(BASE_CODE_DIR):
        raise ValueError("Blocked path access")

    os.makedirs(path, exist_ok=True)

def set_game_mode():
    import subprocess
    import time
    import pyautogui
    PREDATOR_SENSE_PATH = r"C:\Program Files\PredatorSense\Prerequisites\PredatorSenseLauncher.exe"
    subprocess.Popen(PREDATOR_SENSE_PATH)
    time.sleep(5)  # allow app to fully load
    if not pyautogui.getActiveWindow():
        raise Exception("No active window detected")

    SCENARIO_TAB = (245, 29)
    # Click Scenario tab
    pyautogui.moveTo(*SCENARIO_TAB, duration=0.5)
    pyautogui.click()
    time.sleep(1)
    SCENARIO_PROFILE = (367, 84)
    # Select Scenario profile
    pyautogui.moveTo(*SCENARIO_PROFILE, duration=0.5)
    pyautogui.click()
    time.sleep(1)
    GAMING_PROFILE = (292, 177)
    # Select Gaming profile
    pyautogui.moveTo(*GAMING_PROFILE, duration=0.5)
    pyautogui.click()
    time.sleep(1)

def open_vscode(path):
    if not os.path.exists(path):
        raise ValueError(f"Path does not exist: {path}")

    subprocess.Popen([VSCODE_PATH, path])
    time.sleep(1)
    
def save_file(path, filename):
    if not path.startswith("C:\\"):
        raise ValueError("Blocked save location")

    pyautogui.hotkey("ctrl", "s")
    time.sleep(1)

    full_path = os.path.join(path, filename)
    pyautogui.write(full_path)
    pyautogui.press("enter")
    time.sleep(1)



# ---- EXECUTOR ----
def execute_action(step):
    action = step["action"]

    if action == "open_app":
        pyautogui.press("win")
        time.sleep(1)
        pyautogui.write(step["app_name"])
        pyautogui.press("enter")
        time.sleep(2)

    elif action == "type":
        value = step["value"]

        if value == "<ENTER>":
            pyautogui.press("enter")
        else:
            pyautogui.write(value, interval=0.05)

    elif action == "wait":
        time.sleep(step["value"])

    elif action == "move_mouse":
        pyautogui.moveTo(step["x"], step["y"], duration=0.5)

    elif action == "click":
        pyautogui.click()

    elif action == "ensure_folder":
        ensure_folder(step["path"])

    elif action == "open_vscode":
        open_vscode(step["path"])
    elif action == "set_game_mode":
        set_game_mode()
    elif action == "save_file":
        save_file(step["path"], step["filename"])


    else:
        raise ValueError(f"Blocked action: {action}")
