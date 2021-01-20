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
    log_message_entry(message)
    if message.content.startswith(COMMAND_PREFIX):
        normal_dices, hunger_dices = tokenize(without_command_prefix(message.content))
        roll_result = roll(normal_dices, hunger_dices)
        await message.channel.send(f'{message.author.mention} rolled:\n\n{roll_result.stringify()}')


def without_command_prefix(content) -> str:
    return content.lstrip(COMMAND_PREFIX)


def log_message_entry(message):
    print('Message from {0.author}: {0.content}'.format(message))


def tokenize(message: str) -> (int, int):
    """3+2"""
    split = message.split("+")

    normal_dices = int(split[0].strip())
    hunger_dices = 0
    if len(split) > 1:
        hunger_dices = int(split[1].strip())

    return normal_dices, hunger_dices


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
    token = os.getenv('%s' % token_key)
    if not token:
        print(f'please provide a {token_key} environment variable')
        exit(1)

    client.run(token)
