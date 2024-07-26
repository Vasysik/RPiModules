import subprocess
import time
import pyautogui
import json
import os

def update_status(status):
    with open('status.json', 'w') as f:
        json.dump({"status": status}, f)

def read_configuration():
    with open('configuration.json', 'r') as f:
        return json.load(f)

def run_script():
    update_status("running")

    process = subprocess.Popen(['python3', 'hamsterkombat/main.py'])

    time.sleep(2)

    config = read_configuration()

    inputs = []
    if config["Auto Buy Upgrade"] == "ON":
        inputs.extend([1, 1])
    if config["Auto Complete Combo"] == "ON":
        inputs.append(2)
    if config["Auto Complete Cipher"] == "ON":
        inputs.append(3)
    if config["Auto Complete Mini Game"] == "ON":
        inputs.append(4)
    if config["Auto Complete Tasks"] == "ON":
        inputs.append(5)
    
    inputs.append(6)

    for number in inputs:
        pyautogui.write(str(number))
        pyautogui.press('enter')
        time.sleep(1)

    process.wait()

    update_status("not running")
    time.sleep(5)
    run_script()

while True:
    try:
        run_script()
    except Exception as e:
        print(f"Error: {e}")
        update_status("crashed")
        time.sleep(5)
