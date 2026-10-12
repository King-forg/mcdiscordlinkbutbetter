import logging
from mcrcon import MCRcon
import time
import os
import ctypes
import requests

from config import WEBHOOK_URL, HOST, PASSWORD

serveronline = False


class mcrcon:
    """Concrete wrapper around the MCRcon client."""

    def __init__(self, host, password, port=25575, **kwargs):
        self._client = MCRcon(host, password, port=port, **kwargs)

    def connect(self):
        """Open the RCON connection."""
        return self._client.connect()

    def disconnect(self):
        """Close the RCON connection."""
        return self._client.disconnect()

    def command(self, command):
        """Send a command and return the server response."""
        return self._client.command(command)

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()
        return False


def log(message):
    logging.info(message)

while True:
    try:
        with mcrcon(HOST, PASSWORD) as mcr:
            mcr.command("list")

        log("Connection success")
        serveronline = True

        break
    except Exception:
        log("Still offline trying in 10s")
        time.sleep(10)

while True:
    try:
        with mcrcon(HOST, PASSWORD) as mcr:
            response = mcr.command("list")

            log(response)

            if ":" in response:
                players = response.split(":")[1].strip()
                if players == "0":
                    log("No players online")
                else:
                    log(f"{players} players online")
    except Exception as e:
        log(f"Error: {e}")
        

