# mcdiscordlinkbutbetter

Minimal Python project structure for a Minecraft ↔ Discord link bot with commands beyond basic ping/help style commands.

AI used only to route messages to discord but planning on learning how to do myself. Specifically discordsend(message)

Working on the dashboard while using other dashboards as guidance.

## Installation and running

From the project root, create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install --upgrade pip
python -m pip install mcrcon discord.py
```

Set the Minecraft RCON and Discord bot values in
[`dashboard/configbox.py`](dashboard/configbox.py). Do not commit real passwords,
webhook URLs, or bot tokens to the repository.

Start the dashboard from the `dashboard` directory:

```powershell
Set-Location dashboard
python main2.py
```

The program connects to Discord and then displays an interactive menu. Enter
`exit` to stop it.