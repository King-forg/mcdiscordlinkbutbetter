from datetime import datetime
from genericpath import exists
import os
import discord
import subroutines
import configbox

class Client(discord.Client):
    async def on_ready(self):
        subroutines.outputline(f"Logged in as {self.user} (ID: {self.user.id})")
        subroutines.outputline("------")
        subroutines.outputline("Discord bot is ready.")
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
            elif message.content.startswith("/custom"):
                subroutines.outputline(f"Received custom command: {message.content}")
                custom_command = message.content.removeprefix("/custom ")
                await subroutines.custom_command(custom_command)

                
intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(configbox.discord_token)