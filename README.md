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

In VS Code, select the project virtual environment as the Python interpreter:

1. Open the Command Palette with `Ctrl+Shift+P`.
2. Run `Python: Select Interpreter`.
3. Choose `.venv\Scripts\python.exe`.

Install the required packages:

```powershell
python -m pip install --upgrade pip
python -m pip install mcrcon discord.py
```

The package is installed as `discord.py`, but it is imported in Python as
`discord`. Confirm that the selected interpreter can import it:

```powershell
python -c "import discord; print(discord.__version__)"
```

If this check fails, activate `.venv` again and install with `python -m pip`
instead of running `pip` directly. Using `python -m pip` ensures that the
package is installed into the same Python environment that runs the dashboard.

Set the Minecraft RCON and Discord bot values in
[`dashboard/configbox.py`](dashboard/configbox.py). Do not commit real passwords,
webhook URLs, or bot tokens to the repository.

Start the dashboard from the `dashboard` directory:

```powershell
cd dashboard
python main.py
```

Please read error messages if you get them and fix problems it says. If its highlighted in red, change configbox.py
Python may throw out some "global error" errors. It should still work if you run it however if it runs continuously then it is broken. (Feel free to dm me anywhere)

The program connects to Discord and then displays an interactive menu. Enter
`exit` to stop it.
