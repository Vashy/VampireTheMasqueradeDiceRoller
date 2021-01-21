from typing import Final, List, NoReturn
import os

import discord

from VampireDiceRoller.CommandTokenizer import tokenize
from VampireDiceRoller.DiceRoller import roll, RollResult

TOKEN_KEY: Final = 'VTM_BOT_TOKEN'
COMMAND_PREFIX: Final = '/r'

client = discord.Client()


@client.event
async def on_ready():
    print('Logged on as {0.user}!'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(COMMAND_PREFIX):
        log_command_entry(message)
        normal_dices, hunger_dices, comment = tokenize(without_command_prefix(message.content))
        roll_result = roll(normal_dices, hunger_dices)
        await message.channel.send(f'{message.author.mention} rolled{get(comment)}{map_to_str(roll_result.rolls)}'
                                   f':\n\n{stringify(roll_result)}')


def map_to_str(rolls: List[int]) -> str:
    return ' `[' + ', '.join([str(i) for i in rolls]) + ']`'


def without_command_prefix(content: str) -> str:
    return content.lstrip(COMMAND_PREFIX)


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


if __name__ == '__main__':
    client.run(get_token())
