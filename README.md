# Vampire - The Masquerade Dice Roller bot for Discord

## Setup

### Dependencies

* Python 3.8+
* pip

Install requirements (only `discord.py`):

    pip install -r requirements.txt

### Virtualenv (optional)

It's always recommended to activate a `Virtual Environment`:

    virtualenv venv
    # or
    python -m virtualenv venv 

Activate it:

    # GNU/Linux
    ./venv/bin/activate
    
    # Windows
    venv/Scripts/activate

### Token

Provide a valid Discord bot token via the following environment variable: `VTM_BOT_TOKEN`

#### GNU/Linux or Mac OS

    export VTM_BOT_TOKEN="YOUR TOKEN HERE"

#### Windows

    setx VTM_BOT_TOKEN "YOUR TOKEN HERE"

### Launch bot

    python -m VampireDiceRoller.DiscordClient
 
 
 ## Usage example
 
    # /r denotes the command to invoke the bot
    # 3 denotes how many normal dices to roll
    # 2 denotes how many hunger dices to roll
    /r 3+2

    # Without hunger dices
    /r 5
    
    # Comments are allowed
    /r 1+5 You are hungry!

