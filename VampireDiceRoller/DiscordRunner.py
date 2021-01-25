import argparse
from typing import NoReturn

import discord

from VampireDiceRoller.CommandTokenizer import tokenize
from VampireDiceRoller.DiceRoller import roll
from VampireDiceRoller.RunnersUtils import invoking_command_prefix, without_command_prefix, get_api_token
from VampireDiceRoller.Stringifier import build_reply

client = discord.Client()


@client.event
async def on_ready():
    print(f'Logged on as {client.user}!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(invoking_command_prefix()):
        log_command_entry(message)
        normal_dices, hunger_dices, comment = tokenize(without_command_prefix(message.content))
        roll_result = roll(normal_dices, hunger_dices)
        await message.channel.send(build_reply(comment, message.author.mention, roll_result))


def log_command_entry(message: discord.Message) -> NoReturn:
    print(f'Message from {message.author}: {message.content}')


def parse_command_prefix_argument(log: bool = True) -> str:
    parser = argparse.ArgumentParser(description='Customize Command Prefix.')
    parser.add_argument('--command-prefix', nargs='?', help='Pick a custom command prefix (default: /)', default='/')
    prefix = parser.parse_args().command_prefix
    if log:
        print(f'COMMAND_PREFIX: {prefix}')

    return prefix


if __name__ == '__main__':
    COMMAND_PREFIX = parse_command_prefix_argument(log=True)
    client.run(get_api_token())
