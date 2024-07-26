import pexpect
import time
import json

def update_status(status):
    with open('status.json', 'w') as f:
        json.dump({"status": status}, f)

def read_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def run_script():
    update_status("running")

    process = pexpect.spawn('python3 hamsterkombat/main.py')

    config = read_config()

    inputs = []
    if config["Auto Buy Upgrade"] == "ON":
        inputs.extend([1, 1])
    if config["Auto Complete Combo"] == "ON":
        inputs.append(2)
    if config["Auto Complete Cipher"] == "ON":
        inputs.append(3)
    if config["Auto Complete Mini Game"] == "OFF":
        inputs.append(4)
    if config["Auto Complete Tasks"] == "OFF":
        inputs.append(5)

    inputs.append(6)

    for number in inputs:
        process.sendline(str(number))
        time.sleep(1)

    process.expect(pexpect.EOF)

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
