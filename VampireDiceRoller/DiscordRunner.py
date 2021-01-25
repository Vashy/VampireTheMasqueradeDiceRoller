from typing import Final, NoReturn
import os
import argparse

from VampireDiceRoller.CommandTokenizer import tokenize
from VampireDiceRoller.DiceRoller import roll
from VampireDiceRoller.Stringifier import build_reply

import discord

TOKEN_KEY: Final = 'VTM_BOT_TOKEN'
COMMAND_PREFIX = '/'

client = discord.Client()


@client.event
async def on_ready():
    print('Logged on as {0.user}!'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(invoking_command_prefix()):
        log_command_entry(message)
        normal_dices, hunger_dices, comment = tokenize(without_command_prefix(message.content))
        roll_result = roll(normal_dices, hunger_dices)
        await message.channel.send(build_reply(comment, message.author.mention, roll_result))


def log_command_entry(message: str) -> NoReturn:
    print('Message from {0.author}: {0.content}'.format(message))


def invoking_command_prefix() -> str:
    return COMMAND_PREFIX + 'r'


def without_command_prefix(content: str) -> str:
    return content.lstrip(invoking_command_prefix())


def get_token() -> str:
    token = os.getenv(TOKEN_KEY)
    if not token:
        print(f'please provide a {TOKEN_KEY} environment variable')
        exit(1)

    return token


def parse_command_prefix_argument(log: bool = True) -> str:
    parser = argparse.ArgumentParser(description='Customize Command Prefix.')
    parser.add_argument('--command-prefix', nargs='?', help='Pick a custom command prefix (default: /)', default='/')
    prefix = parser.parse_args().command_prefix
    if log:
        print(f'COMMAND_PREFIX: {prefix}')

    return prefix


if __name__ == '__main__':
    COMMAND_PREFIX = parse_command_prefix_argument(log=True)
    client.run(get_token())
