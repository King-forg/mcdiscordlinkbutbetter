import time
import mcrcon

while True:
    try:
        with mcrcon(HOST, PASSWORD) as mcr:
            response = mcr.command("list")
            log(f"Server response: {response}")
            time.sleep(10)
    except Exception:
        log("Connection lost, trying to reconnect in 10s")
        serveronline = False
        time.sleep(10)
    try:
        with mcrcon(HOST, PASSWORD) as mcr:
            response = mcr.