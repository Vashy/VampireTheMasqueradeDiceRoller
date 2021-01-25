import logging
from typing import Final, NoReturn

import telegram.ext

from VampireDiceRoller.CommandTokenizer import tokenize
from VampireDiceRoller.DiceRoller import roll
from VampireDiceRoller.RunnersUtils import without_command_prefix, get_api_token
from VampireDiceRoller.Stringifier import build_reply

TOKEN_KEY: Final = 'VTM_BOT_TOKEN'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def roll_command_handler(update_obj: telegram.Update, _: telegram.ext.CallbackContext):
    log_command_entry(update_obj)
    normal_dices, hunger_dices, comment = tokenize(without_command_prefix(update_obj.message.text, prefix='/'))
    roll_result = roll(normal_dices, hunger_dices)
    update_obj.message.reply_markdown_v2(build_reply(comment,
                                                     user_mention=None,
                                                     roll_result=roll_result,
                                                     list_prefix='\\-',
                                                     bold_delimiter='*',
                                                     italic_delimiter='_'),
                                         quote=True)


def log_command_entry(update: telegram.Update) -> NoReturn:
    print(f'Message from {update.message.from_user.username}: {update.message.text}')


if __name__ == '__main__':
    updater = telegram.ext.Updater(get_api_token())
    dispatcher = updater.dispatcher
    dispatcher.add_handler(telegram.ext.CommandHandler(
        command='r',
        callback=roll_command_handler,
    ))
    updater.start_polling()
    updater.idle()
