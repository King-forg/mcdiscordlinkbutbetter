import asyncio
import configbox
import datetime
import discord
import re
from pathlib import Path
from mcrcon import MCRcon


LOG_DIR = Path(__file__).resolve().parent.parent / "log"
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "log.txt"

if LOG_FILE.exists():
    rotated_log = LOG_DIR / f"log{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    LOG_FILE.rename(rotated_log)

def _get_player_count():
    try:
        with MCRcon(configbox.domain, configbox.secret) as mcr:
            response = mcr.command("list")
            match = re.search(r"There are (\d+)", response)
            if match:  
                count = match.group(1)
                outputline(f"Current player count: {count}")
                return count
            else:
                outputline("Couldn't parse server response")
                return None
    except Exception as e:
        outputline(f"Error: {e}")
        global errors
        errors = True
        return None

async def get_player_count():
    return await asyncio.to_thread(_get_player_count)

def mcserverconnection():
    try:
        with MCRcon(configbox.domain, configbox.secret) as mcr:
            response = mcr.command("list")
            outputline(f"Successfully connected to the Minecraft server. Response: {response}")
    except Exception as e:
        outputline(f"Error connecting to the Minecraft server: {e}")
        global errors
        errors = True

def outputline(line):
    print(line)
    with LOG_FILE.open("a") as writefile:
        writefile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + line + "\n")

def restart_server():
    try:
        with MCRcon(configbox.domain, configbox.secret) as mcr:
            response = mcr.command("restart")
            outputline(f"Server started. Response: {response}")
    except Exception as e:
        outputline(f"Error stopping the server: {e}")
        global errors
        errors = True

def stop_server():
    try:
        with MCRcon(configbox.domain, configbox.secret) as mcr:
            response = mcr.command("stop")
            outputline(f"Server stopped. Response: {response}")
    except Exception as e:
        outputline(f"Error stopping the server: {e}")
        global errors
        errors = True

def get_whitelist():
    playerselect = input("Enter player name: ")
    with MCRcon(configbox.domain, configbox.secret) as mcr:
        response = mcr.command(f"whitelist list")
        match = re.search(playerselect, response)
        if match:
            outputline(f"{playerselect} is whitelisted")
            if playerselect == "":
                try:
                    with MCRcon(configbox.domain, configbox.secret) as mcr:
                        response = mcr.command(f"list")
                        match = re.search(playerselect, response)
                        if match:
                            outputline(f"{playerselect} is online")
                        else:
                            outputline(f"{playerselect} is offline")
                except Exception as e:
                    outputline(f"Error: {e}")
        else:
            outputline(f"{playerselect} is not whitelisted")

def _whitelist_player(whitelistplayer):
    try:
        with MCRcon(configbox.domain, configbox.secret) as mcr:
            response = mcr.command(f"whitelist add {whitelistplayer}")
            if "Added" in response:
                outputline(f"{whitelistplayer} has been whitelisted")
            else:
                outputline(f"Failed to whitelist {whitelistplayer}. Response: {response}")
    except Exception as e:
        outputline(f"Error: {e}")
        global errors
        errors = True

def get_server_status():
    try:
        with MCRcon(configbox.domain, configbox.secret) as mcr:
            response = mcr.command("list")
            if "There are" in response:
                return "Online"
            else:
                return "Offline"
    except Exception as e:
        outputline(f"Error: {e}")
        global errors
        errors = True
        return "Error"

async def whitelist_player(whitelistplayer):
    return await asyncio.to_thread(_whitelist_player, whitelistplayer)

def _remove_whitelist_player(whitelistplayer):
    try:
        with MCRcon(configbox.domain, configbox.secret) as mcr:
            response = mcr.command(f"whitelist remove {whitelistplayer}")
            if "Removed" in response:
                outputline(f"{whitelistplayer} has been removed from the whitelist")
            else:
                outputline(f"Failed to remove {whitelistplayer} from the whitelist. Response: {response}")
    except Exception as e:
        outputline(f"Error: {e}")
        global errors
        errors = True

async def remove_whitelist_player(whitelistplayer):
    return await asyncio.to_thread(_remove_whitelist_player, whitelistplayer)

def _custom_command(custom_command):
    try:
        with MCRcon(configbox.domain, configbox.secret) as mcr:
            response = mcr.command(custom_command)
            outputline(f"Response: {response}")
            if response == "":
                outputline("Probably worked for some commands, but not all. Check the server for results.")
            if "Error" in response:
                outputline(f"Error executing command: {response}")
                custom()
    except Exception as e:
        outputline(f"Error: {e}")
        global errors
        errors = True

async def custom_command(custom_command):
    return await asyncio.to_thread(_custom_command, custom_command)