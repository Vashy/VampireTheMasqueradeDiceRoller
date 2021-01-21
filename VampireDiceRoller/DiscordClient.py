from typing import Final, List
import os

import discord

from VampireDiceRoller.DiceRoller import roll, RollResult

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
        await message.channel.send(f'{message.author.mention} rolled{get(comment)}:\n\n{stringify(roll_result)}')


def without_command_prefix(content) -> str:
    return content.lstrip(COMMAND_PREFIX)


def get(comment: str) -> str:
    if comment:
        return f' {comment}'
    else:
        return ''


def log_command_entry(message):
    print('Message from {0.author}: {0.content}'.format(message))


def tokenize(message: str) -> (int, int, str):
    """3+2"""
    split = message.split('+')
    if len(split) == 1:
        comment, normal_dices = split_comment_and_dices(split[0].strip())
        return normal_dices, 0, comment
    else:
        normal_dices = int(split[0].strip())
        comment = None
        if len(split) > 1:
            comment, hunger_dices = split_comment_and_dices(split[1].strip())
        else:
            hunger_dices = int(split[1].strip())
        return normal_dices, hunger_dices, comment


def split_comment_and_dices(token: str) -> (str, str):
    comment = None
    split = token.split(' ', 1)
    if len(split) > 1:
        comment = f'`{split[1]}`'
    hunger_dices = int(split[0].strip())
    return comment, hunger_dices


def stringify(roll_result: RollResult) -> str:
    result = f"- **Successes**: {roll_result.successes}\n- **Failures**: {roll_result.failures}"
    specials = _find_specials(roll_result)
    if specials:
        result += "\n- **Special**: " + ', '.join(specials)
    return result


def _find_specials(self: RollResult) -> List[str]:
    specials = []
    if self.is_critical:
        specials.append("*critical hit*")
    if self.is_messy_critical:
        specials.append("*messy critical*")
    if self.is_bestial_failure:
        specials.append("*bestial failure*")
    return specials


if __name__ == '__main__':
    token_key = 'VTM_BOT_TOKEN'
    token = os.getenv(token_key)
    if not token:
        print(f'please provide a {token_key} environment variable')
        exit(1)

    client.run(token)
