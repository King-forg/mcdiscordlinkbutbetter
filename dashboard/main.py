from datetime import datetime, time
from genericpath import exists
import os
import discord
import subroutines
import configbox

demomode = input("Attempting to connect to discord bot. You can use demomode if you have not set up a discord bot yet. Do you want to use demomode? (y/n): ")
if demomode.lower() == "y":
    print("Demomode enabled. Discord bot will not be connected.")
    demomode = True
else:
    demomode = False

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
client.run(configbox.discord_token)
