from typing import Optional


def split_comment_and_dices(token: str) -> (str, str):
    comment = None
    split = token.split(' ', 1)
    if len(split) > 1:
        comment = f'{split[1]}'
    hunger_dices = int(split[0].strip())
    return comment, hunger_dices


def tokenize(message: str) -> (int, int, Optional[str]):
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
