# Vampire - The Masquerade Dice Roller bot for Discord

## Dependencies

* Python 3.8+
* pip

Install requirements (only `discord.py`):

    pip install -r requirements.txt

### Virtualenv

It's always recommended to activate a `Virtual Environment`:

    virtualenv venv
    # or
    python -m virtualenv venv 

Activate it:

    # GNU/Linux
    ./venv/bin/activate
    
    # Windows
    venv/Scripts/activate

## Setup

Provide a valid Discord bot token via the following environment variable: `VTM_BOT_TOKEN`

### GNU/Linux or Mac OS

    export VTM_BOT_TOKEN="YOUR TOKEN HERE"

### Windows

    setx VTM_BOT_TOKEN "YOUR TOKEN HERE"

## Launch bot

    python -m VampireDiceRoller.DiscordClient
 
