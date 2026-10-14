from cmath import log
from genericpath import exists
from multiprocessing.util import debug
import os
from mcrcon import MCRcon
import re
import configbox
import datetime

errors = False

if exists("log.txt") == True:
    os.rename("log.txt", "log" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".txt")

open("log.txt", "w")

def outputline(line):
    print(line)
    with open("log.txt", "a") as writefile:
        writefile.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " " + line + "\n")

def discordsend(message):
    import json
    from urllib.error import HTTPError, URLError
    from urllib.request import Request, urlopen

    data = {"content": message}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    request = Request(
        configbox.webhook_url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urlopen(request) as response:
            if response.status != 204:
                outputline(f"Failed to send message to Discord. Status code: {response.status}")
    except HTTPError as error:
        outputline(f"Failed to send message to Discord. Status code: {error.code}")
    except URLError as error:
        outputline(f"Failed to send message to Discord: {error.reason}")

def get_player_count():
    try:
        with MCRcon(configbox.domain, configbox.secret) as mcr:
            response = mcr.command("list")
            if debug == True:
                outputline(f"Raw server response: {response}")

            match = re.search(r"There are (\d+)", response)
            if match:
                if debug == True:
                    outputline(f"Parsed player count: {match.group(1)}")
                count = int(match.group(1))
                outputline(f"Current player count: {count}")
                if debug == True:
                    outputline(f"Sending message to Discord: Current player count: {count}")
                discordsend(f"Current player count: {count}")
                return count
            else:
                if debug == True:
                    outputline("Couldn't parse server response")
                outputline("Couldn't parse server response")
                outputline(f"Raw output: {response}")
                discordsend(f"Couldn't parse server response: {response}")
                return None
    except Exception as e:
        outputline(f"Error: {e}")
        discordsend(f"Error: {e}")
        global errors
        errors = True
        return None

def get_whitelist():
    playerselect = input("Enter player name: ")
    with MCRcon(configbox.domain, configbox.secret) as mcr:
        response = mcr.command(f"whitelist list")
        outputline(f"Raw whitelist response: {response}")
        match = re.search(playerselect, response)
        if match:
            outputline(f"{playerselect} is whitelisted")
            discordsend(f"{playerselect} is whitelisted")
            if playerselect == "":
                try:
                    with MCRcon(configbox.domain, configbox.secret) as mcr:
                        response = mcr.command(f"list")
                        match = re.search(playerselect, response)
                        if match:
                            outputline(f"{playerselect} is online")
                            discordsend(f"{playerselect} is online")
                        else:
                            outputline(f"{playerselect} is offline")
                            discordsend(f"{playerselect} is offline")
                except Exception as e:
                    outputline(f"Error: {e}")
        else:
            outputline(f"{playerselect} is not whitelisted")
            discordsend(f"{playerselect} is not whitelisted")

def whitelist_player():
    whitelistplayer = input("Enter player name to whitelist: ")
    try:
        with MCRcon(configbox.domain, configbox.secret) as mcr:
            response = mcr.command(f"whitelist add {whitelistplayer}")
            if "Added" in response:
                outputline(f"{whitelistplayer} has been whitelisted")
                discordsend(f"{whitelistplayer} has been whitelisted")
            else:
                outputline(f"Failed to whitelist {whitelistplayer}. Response: {response}")
                discordsend(f"Failed to whitelist {whitelistplayer}. Response: {response}")
    except Exception as e:
        outputline(f"Error: {e}")
        discordsend(f"Error: {e}")
        global errors
        errors = True

def remove_whitelist_player():
    whitelistplayer = input("Enter player name to remove from whitelist: ")
    try:
        with MCRcon(configbox.domain, configbox.secret) as mcr:
            response = mcr.command(f"whitelist remove {whitelistplayer}")
            if "Removed" in response:
                outputline(f"{whitelistplayer} has been removed from the whitelist")
                discordsend(f"{whitelistplayer} has been removed from the whitelist")
            else:
                outputline(f"Failed to remove {whitelistplayer} from the whitelist. Response: {response}")
                discordsend(f"Failed to remove {whitelistplayer} from the whitelist. Response: {response}")
    except Exception as e:
        outputline(f"Error: {e}")
        discordsend(f"Error: {e}")
        global errors
        errors = True

def custom():
    custom_command = input("Enter custom command for in game.")
    try:
        with MCRcon(configbox.domain, configbox.secret) as mcr:
            response = mcr.command(custom_command)
            outputline(f"Response: {response}")
            discordsend(f"Response: {response}")
            if response == "":
                outputline("Probably worked for some commands, but not all. Check the server for results.")
                discordsend("Probably worked for some commands, but not all. Check the server for results.")
            if "Error" in response:
                outputline(f"Error executing command: {response}")
                discordsend(f"Error executing command: {response}")
                custom()
    except Exception as e:
        outputline(f"Error: {e}")
        discordsend(f"Error: {e}")
        global errors
        errors = True

def main():
    while True:    
        selection = input("Select an option:\n1. Get player count\n2. Check whitelist\n3. Whitelist a player\n4. Remove a player from whitelist\n5. Send a message to Discord\n6. Custom option\n Enter your choice (1-6): \n\n\n")
        if selection == "1":
            get_player_count()
        elif selection == "2":
            get_whitelist()
        elif selection == "3":
            whitelist_player()
        elif selection == "4":
            remove_whitelist_player()
        elif selection == "5":
            message = input("Enter the message to send to Discord: ")
            discordsend(message)
        elif selection == "6":
            outputline("Custom selected.")
            custom()
        elif selection == "exit":
            outputline("Exiting the program.")
            break
        elif selection == "debug":
            outputline("Debug mode activated. Select an option to test.")
            debug = True
        else: 
            outputline("Invalid choice. Please enter a number between 1 and 6.")

main()