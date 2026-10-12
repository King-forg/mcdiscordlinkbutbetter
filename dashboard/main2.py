from mcrcon import MCRcon

domain = "mc.kingf.org"
port = 25575
secret = "*****"
webhook_url = "webhookurl"

errors = False

def discordsend(message):
    import requests
    data = {"content": message}
    response = requests.post(webhook_url, json=data)
    if response.status_code != 204:
        print(f"Failed to send message to Discord. Status code: {response.status_code}")





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
    print(f"Raw output: {response}")
    discordsend(f"Error: {e}")
    errors = True
    return None

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
    errors = True

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
    errors = True

    