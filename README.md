# mcdiscordlinkbutbetter

A Minecraft-to-Discord link bot with commands for managing a Minecraft server
from Discord.

## Installation

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

The package is named `discord.py`, but it is imported in Python as `discord`.
Confirm that the selected interpreter can import it:

```powershell
python -c "import discord; print(discord.__version__)"
```

If this check fails, activate `.venv` again and install the packages with
`python -m pip`. This ensures they are installed in the same environment used
to run the dashboard.

## Configuration

Set the Minecraft RCON and Discord bot values in
[`dashboard/configbox.py`](dashboard/configbox.py).

Do not commit real passwords, webhook URLs, or bot tokens to the repository.

## Running the dashboard

Start the dashboard from the `dashboard` directory:

```powershell
cd dashboard
python main.py
```

## Troubleshooting

* If VS Code reports `Import "discord" could not be resolved`, select
  `.venv\Scripts\python.exe` with **Python: Select Interpreter**.
* If the problem continues, activate `.venv` and reinstall the dependencies:

  ```powershell
  .\.venv\Scripts\Activate.ps1
  python -m pip install --upgrade pip
  python -m pip install discord.py 
  python -m pip install mcrcon
  python -m pip install colorama
  ```

* Check `configbox.py` if the program reports missing or invalid settings.

The program connects to Discord and then displays an interactive menu. Enter
`exit` to stop it.