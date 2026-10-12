from mcrcon import MCRcon
import re

domain = "domain"
port = 25575
secret = "secret"
webhook_url = "webhook"

errors = False

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
        webhook_url,
        data=json.dumps(data).encode("utf-8"),
        headers=headers,
        method="POST",
    )
    try:
        with urlopen(request) as response:
            if response.status != 204:
                print(f"Failed to send message to Discord. Status code: {response.status}")
    except HTTPError as error:
        print(f"Failed to send message to Discord. Status code: {error.code}")
    except URLError as error:
        print(f"Failed to send message to Discord: {error.reason}")




def get_player_count():
    try:
        with MCRcon(domain, secret) as mcr:
            response = mcr.command("list")

            match = re.search(r"There are (\d+)", response)
            if match:
                count = int(match.group(1))
                discordsend(f"Current player count: {count}")
                return count
            else:
                print("Couldn't parse server response")
                print(f"Raw output: {response}")
                discordsend(f"Couldn't parse server response: {response}")
                return None
    except Exception as e:
        print(f"Error: {e}")
        discordsend(f"Error: {e}")
        global errors
        errors = True
        return None

def get_whitelist():
    playerselect = input("Enter player name: ")
    with MCRcon(domain, secret) as mcr:
        response = mcr.command(f"whitelist list")
        match = re.search(playerselect, response)
        if match:
            print(f"{playerselect} is whitelisted")
            discordsend(f"{playerselect} is whitelisted")
            if playerselect == "":
                try:
                    with MCRcon(domain, secret) as mcr:
                        response = mcr.command(f"list")
                        match = re.search(playerselect, response)
                        if match:
                            print(f"{playerselect} is online")
                            discordsend(f"{playerselect} is online")
                        else:
                            print(f"{playerselect} is offline")
                            discordsend(f"{playerselect} is offline")
                except Exception as e:
                    print(f"Error: {e}")
        else:
            print(f"{playerselect} is not whitelisted")
            discordsend(f"{playerselect} is not whitelisted")

def whitelist_player():
    whitelistplayer = input("Enter player name to whitelist: ")
    try:
        with MCRcon(domain, secret) as mcr:
            response = mcr.command(f"whitelist add {whitelistplayer}")
            if "Added" in response:
                print(f"{whitelistplayer} has been whitelisted")
                discordsend(f"{whitelistplayer} has been whitelisted")
            else:
                print(f"Failed to whitelist {whitelistplayer}. Response: {response}")
                discordsend(f"Failed to whitelist {whitelistplayer}. Response: {response}")
    except Exception as e:
        print(f"Error: {e}")
        discordsend(f"Error: {e}")
        global errors
        errors = True

def remove_whitelist_player():
    whitelistplayer = input("Enter player name to remove from whitelist: ")
    try:
        with MCRcon(domain, secret) as mcr:
            response = mcr.command(f"whitelist remove {whitelistplayer}")
            if "Removed" in response:
                print(f"{whitelistplayer} has been removed from the whitelist")
                discordsend(f"{whitelistplayer} has been removed from the whitelist")
            else:
                print(f"Failed to remove {whitelistplayer} from the whitelist. Response: {response}")
                discordsend(f"Failed to remove {whitelistplayer} from the whitelist. Response: {response}")
    except Exception as e:
        print(f"Error: {e}")#
        discordsend(f"Error: {e}")
        global errors
        errors = True

def main():
    while True:    
        selection = input("Select an option:\n1. Get player count\n2. Check whitelist\n3. Whitelist a player\n4. Remove a player from whitelist\n5. Send a message to Discord\n Enter your choice (1-5): \n\n\n")
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
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

main()