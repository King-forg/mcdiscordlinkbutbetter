# mcdiscordlinkbutbetter

`mcdiscordlinkbutbetter` connects a Minecraft server to Discord. It relays
Minecraft chat to Discord, sends Discord chat to Minecraft, and lets a
configured Discord channel run common server-management commands through RCON.

## Requirements

- Windows
- Python 3.10 or newer
- A Minecraft Java server with RCON enabled
- A Discord application and bot
- The bot running on the same computer as the Minecraft server, or on a
  computer that can access the server's RCON port and log file

## Installation

### From the repository

1. Install Python from [python.org](https://www.python.org/downloads/). During
   installation, enable **Add Python to PATH**.
2. Clone or download this repository.
3. Open PowerShell in the repository root.
4. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

5. Install the dependencies:

   ```powershell
   python -m pip install --upgrade pip
   python -m pip install discord.py mcrcon colorama
   ```

If PowerShell prevents the activation script from running, either allow local
scripts for your user or run the commands with the Python executable directly:

```powershell
.\.venv\Scripts\python.exe -m pip install discord.py mcrcon colorama
```

### From a release archive

Download and extract the latest release archive to the computer that hosts the
Minecraft server. Open PowerShell in the extracted folder and install the
dependencies using the commands above. Do not run the bot from inside the
compressed archive.

## Discord bot setup

1. Create an application in the [Discord Developer
   Portal](https://discord.com/developers/applications).
2. Create a bot and copy its token.
3. Enable the **Message Content Intent** under the bot's privileged gateway
   intents. The application uses message content to receive commands and relay
   chat.
4. Invite the bot to your server with permission to view channels, read
   message history, and send messages in the configured chat and command
   channels.
5. Copy the IDs of the chat channel, command channel, and user. The user ID is
   retained in the configuration for future access control.
   Discord Developer Mode must be enabled to copy IDs.

## Minecraft RCON setup

In the Minecraft server's `server.properties`, configure RCON, for example:

```properties
enable-rcon=true
rcon.port=25575
rcon.password=replace-with-a-long-random-password
```

Restart the Minecraft server after changing `server.properties`. The RCON
password and port in `dashboard/configbox.py` must match the server settings.
The configured `logpath` must point to the server's `latest.log` file or its
`logs` directory.

## Configuration

Edit [`dashboard/configbox.py`](dashboard/configbox.py) and replace every
placeholder value:

| Setting | Description |
| --- | --- |
| `chat_id` | Discord channel ID for Minecraft chat relay |
| `commandid` | Discord channel ID where commands are accepted |
| `userid` | Discord user ID reserved for future access control |
| `discord_token` | Discord bot token |
| `logpath` | Path to `latest.log` or the Minecraft `logs` directory |
| `domain` | Minecraft server hostname or IP address used for RCON |
| `port` | RCON port; it must match `server.properties` |
| `secret` | Minecraft RCON password |

Keep `configbox.py` private. Never commit bot tokens, RCON passwords, webhook
URLs, or other credentials. If a token or password has been exposed, rotate it
before running the bot.

## Running the bot

From the repository root with the virtual environment activated:

```powershell
cd dashboard
python main.py
```

On startup, the program asks whether to use demo mode:

- Answer `n` to connect to Discord and Minecraft normally.
- Answer `y` to start without connecting the Discord bot. Demo mode is useful
  for checking the startup flow, but it cannot relay chat or control a server.

The bot writes its runtime log to `log/log.txt` and rotates the previous log
when it starts. Enter `exit` at the local console to stop the program.

## Discord commands

Commands are accepted in the configured command channel. A leading `!` or `/`
is optional. The current command handler does not yet restrict commands by
`userid`, so protect the command channel with Discord permissions.

| Command | Description |
| --- | --- |
| `help` | Show the available commands |
| `list` | List online players |
| `playercount` | Show the current player count |
| `status` | Show whether the server is online |
| `whitelist list` | List whitelisted players |
| `whitelist add <player>` | Add a player to the whitelist |
| `whitelist remove <player>` | Remove a player from the whitelist |
| `restart` | Restart the server after a short delay |
| `stop` | Stop the server after a short delay |
| `custom <command>` | Send a custom Minecraft command through RCON |

Messages posted in the configured chat channel are sent to Minecraft. New
player chat lines from `latest.log` are posted back to that same Discord
channel.

## Troubleshooting

- **`Import "discord" could not be resolved`:** Select
  `.venv\Scripts\python.exe` in VS Code with **Python: Select Interpreter**, then
  reinstall the dependencies using `python -m pip`.
- **The bot does not connect:** Check the token, enable Message Content Intent,
  and confirm that the bot was invited to the correct Discord server.
- **Commands do not work:** Verify `commandid` and `chat_id`. The message must
  be posted in the configured command channel. Use Discord channel permissions
  to restrict who can post commands.
- **RCON errors:** Confirm `enable-rcon=true`, the RCON port and password, the
  server address, and that the Minecraft server was restarted after changing
  `server.properties`.
- **Chat relay is empty:** Check that `logpath` points to the active
  `latest.log` file or its `logs` directory and that the bot can read it.
- **The bot starts in demo mode:** Run `python main.py` again and answer `n`
  when prompted.
