from mcrcon import MCRcon

domain = "mc.kingf.org"
port = 25575
secret = "*****"
webhook_url = "https://discord.com/api/webhooks/1559206097192230935/akpdm6-uxFkpw7fsjbjpPOr8du-ayC3BKWbvLlLX2ugG2ToyRBMxTzv7QMeFyTs7QxAS"


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
    return None

playerselect = input("Enter player name: ")

with MCRcon(domain, secret) as mcr:
    response = mcr.command(f"whitelist list")
    match = re.search(playerselect, response)
    if match:
        print(f"{playerselect} is whitelisted")
        if playerselect == "":
            try:
                with MCRcon(domain, secret) as mcr:
                    response = mcr.command(f"list")
                    match = re.search(playerselect, response)
                    if match:
                        print(f"{playerselect} is online")
                    else:
                        print(f"{playerselect} is offline")
            except Exception as e:
                print(f"Error: {e}")
        
    else:
        print(f"{playerselect} is not whitelisted")
    