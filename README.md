<h1 align="center">Pingbot</h1>
<i><p align="center" >A discord bot to check if a server is open</p></i>

<p align="center">
    <img align="center" src="assets/Animation.gif">
</p>

## Requirements:
- A discord bot token
- A .env file with the syntax:
    ```
    DISCORD_TOKEN=""
    ```
    - Where DISCORD_TOKEN is the token of your discord bot

- Python packages
  - [setproctitle](https://pypi.org/project/setproctitle/)
  - [discordpy](https://pypi.org/project/discord.py/)

## How to use:
- Replace in network.txt the host and the port to check
- Run the bot with `python3 main.py`
- Send `ping` to a channel to check server availavility