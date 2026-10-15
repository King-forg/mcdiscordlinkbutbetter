from datetime import datetime, time
from genericpath import exists
import os
import colorama
import discord
import subroutines
import configbox
from colorama import Fore, Back, Style

errors = 0

demomode = input(Back.GREEN + Fore.RED + "Attempting to connect to discord bot. You can use demomode if you have not set up a discord bot yet. Do you want to use demomode? (y/n): ")
if configbox.discord_token == "placeholder":
    print(Back.RED + Fore.GREEN + "You haven't changed the Discord token value! Please change or continue on demo mode.")
    errors = errors+1
if configbox.domain == "0.0.0.0":
    print(Back.RED + Fore.GREEN + "You haven't changed the domain value! Please change or continue on demo mode.")
    errors = errors+1
if configbox.secret == "placeholder":
    print(Back.RED + Fore.GREEN + "You haven't changed the secret value! Please change or continue on demo mode.")
    errors = errors+1
if configbox.chat_id == "placeholder":
    print(Back.RED + Fore.GREEN + "Still placeholder for chat_id but program will still run (Might break.)")
    errors = errors+1
if configbox.port == 25575:
    print(Back.RED + Fore.GREEN + "Port is 25575. Will work if port in server.properties is set to 25575.")
    errors = errors+1
if errors > 4:
    print(Back.RED + Fore.GREEN + Style.BRIGHT + "Many errors in configbox. Please double check that fields are entered correctly and are actually set to proper values.")
print(Style.RESET_ALL + ".")
if demomode.lower() == "y":
    print("Demomode enabled. Discord bot will not be connected.")
    demomode = True
else:
    demomode = False
subroutines.set_demomode(demomode)

class Client(discord.Client):
    async def on_ready(self):
        subroutines.outputline(f"Logged in as {self.user} (ID: {self.user.id})")
        subroutines.outputline("------")
        subroutines.outputline("Discord bot is ready.")
        if not demomode:
            subroutines.mcserverconnection()

    async def on_message(self, message):
        if message.author == self.user:
            return
        elif message.author.id == int(configbox.userid):
            if message.content.startswith("/whitelist add"):
                subroutines.outputline(f"Received whitelist add command: {message.content}")
                whitelistplayer = message.content.removeprefix("/whitelist add ")
                await subroutines.whitelist_player(whitelistplayer)
                await message.channel.send(f"Added {whitelistplayer} to the whitelist.")
            elif message.content.startswith("/whitelist remove"):
                subroutines.outputline(f"Received whitelist remove command: {message.content}")
                whitelistplayer = message.content.removeprefix("/whitelist remove ")
                await subroutines.remove_whitelist_player(whitelistplayer)
                await message.channel.send(f"Removed {whitelistplayer} from the whitelist.")
            elif message.content.startswith("/playercount"):
                subroutines.outputline(f"Received player count command: {message.content}")
                player_count = await subroutines.get_player_count()
                await message.channel.send(f"Current player count: {player_count}")
            elif message.content.startswith("/whitelist list"):
                subroutines.outputline(f"Received whitelist list command: {message.content}")
                await subroutines.get_whitelist()
            elif message.content.startswith("/list"):
                subroutines.outputline(f"Received list command: {message.content}")
                await subroutines.get_online_players()
            elif message.content.startswith("/help"):
                subroutines.outputline(f"Received help command: {message.content}")
                help_message = (
                    "Available commands:\n"
                    "/whitelist add <player> - Add a player to the whitelist.\n"
                    "/whitelist remove <player> - Remove a player from the whitelist.\n"
                    "/whitelist list - List all whitelisted players.\n"
                    "/list - List all online players.\n"
                    "/playercount - Get the current player count.\n"
                    "/custom <command> - Execute a custom command on the server."
                )
                await message.channel.send(help_message)
            elif message.content.startswith("/restart"):
                subroutines.outputline(f"Received restart command. Restarting server in 3s...")
                time.sleep(3)
                await subroutines.restart_server()
            elif message.content.startswith("/stop"):
                subroutines.outputline(f"Received stop command. Stopping server in 3s...")
                time.sleep(3)
                await subroutines.stop_server()
            elif message.content.startswith("/status"):
                subroutines.outputline(f"Received status command: {message.content}")
                server_status = await subroutines.get_server_status()
                await message.channel.send(f"Server status: {server_status}")
            elif message.content.startswith("/custom"):
                subroutines.outputline(f"Received custom command: {message.content}")
                custom_command = message.content.removeprefix("/custom ")
                await subroutines.custom_command(custom_command)

                
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
try:
    client.run(configbox.discord_token)
except:
    if configbox.discord_token == "placeholder":
        print(Back.RED + Fore.GREEN + "Please set discord token in configbox")
        print(Style.RESET_ALL + ".")
    else:
        print(Back.RED + Fore.GREEN + "Fatal Error. Check token is valid or is typed correctly.")
        print(Style.RESET_ALL + ".")
    if demomode == True:
        print(
        "Available commands:\n"
        "get_player_count() - Add a player to the whitelist.\n"
        "remove_whitelist_player(whitelistplayer) - Remove a player from the whitelist.\n"
        "get_whitelist(playerselect) - List all whitelisted players.\n"
        "whitelist_player(whitelistplayer) - Whitelist a player. \n"
        "get_online_players() - List all online players.\n"
        "get_player_count() - Get the current player count.\n"
        "custom_command - Execute a custom command on the server.")
        while demomode == True:
            command = input("Enter command: ")
            print("Recieved command: " + command)
            print(colorama.Fore.YELLOW + "Demomode is enabled. Message recieved but cannot be processed because the discord bot is not connected to a Minecraft server. Please set up a discord bot and connect it to a Minecraft server to use this feature.")
            print(colorama.Style.RESET_ALL)
            if command == "exit":
                demomode = False
    
 
