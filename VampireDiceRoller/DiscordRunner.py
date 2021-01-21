from typing import Final, List, NoReturn
import os
import argparse

import discord

from VampireDiceRoller.CommandTokenizer import tokenize
from VampireDiceRoller.DiceRoller import roll, RollResult

TOKEN_KEY: Final = 'VTM_BOT_TOKEN'
COMMAND_PREFIX = None

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
        await message.channel.send(f'{message.author.mention} rolled{get(comment)}{map_to_str(roll_result.rolls)}'
                                   f':\n\n{stringify(roll_result)}')


def invoking_command_prefix():
    return COMMAND_PREFIX + 'r'


def map_to_str(rolls: List[int]) -> str:
    return ' `[' + ', '.join([str(i) for i in rolls]) + ']`'


def without_command_prefix(content: str) -> str:
    return content.lstrip(invoking_command_prefix())


def get(comment: str) -> str:
    if comment:
        return f" *'{comment}'*"
    else:
        return ''


def log_command_entry(message: str) -> NoReturn:
    print('Message from {0.author}: {0.content}'.format(message))


def stringify(roll_result: RollResult) -> str:
    result = f"- **Successes**: {roll_result.successes}\n- **Failures**: {roll_result.failures}"
    specials = _list_specials(roll_result)
    if specials:
        result += "\n- **Special**: " + ', '.join(specials)
    return result


def _list_specials(self: RollResult) -> List[str]:
    specials = []
    if self.is_critical:
        specials.append("*critical hit*")
    if self.is_messy_critical:
        specials.append("*messy critical*")
    if self.is_bestial_failure:
        specials.append("*bestial failure*")
    return specials


def get_token():
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
