import pexpect, time, json, sys, re

def update_status(status, end_string=""):
    with open('status.json', 'w') as f:
        json.dump({"status": status, "endString": end_string}, f)

def read_config():
    with open('config.json', 'r') as f:
        return json.load(f)
    
def remove_ansi_sequences(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def run_script():
    update_status("running")

    process = pexpect.spawn('python3 hamsterkombat/main.py', logfile=sys.stdout, encoding='utf-8')

    config = read_config()

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
        process.sendline(str(number))
        time.sleep(1)

    while True:
        try:
            process.expect(pexpect.TIMEOUT, timeout=1)
            last_line = remove_ansi_sequences(process.before).splitlines()[-1]
            update_status("running", last_line)
        except pexpect.TIMEOUT:
            continue
        except pexpect.EOF:
            break

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
