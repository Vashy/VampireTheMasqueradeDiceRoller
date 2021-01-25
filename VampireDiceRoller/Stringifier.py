from typing import List

from VampireDiceRoller.DiceRoller import RollResult


def build_reply(comment: str,
                user_mention: str,
                roll_result: RollResult,
                bold_delimiter: str = '**',
                italic_delimiter: str = '*') -> str:
    comment = _parse(comment, italic_delimiter)
    rolls_as_str = _map_to_str(roll_result.rolls)

    return f'{user_mention} rolled{comment}{rolls_as_str}:\n\n' \
           f'{stringify(roll_result, bold_delimiter, italic_delimiter)}'


def stringify(roll_result: RollResult, bold_delimiter: str = '**', italic_delimiter: str = '*',
              list_prefix: str = '-') -> str:
    result = f"{list_prefix} {bold_delimiter}Successes{bold_delimiter}: {roll_result.successes}\n" \
             f"{list_prefix} {bold_delimiter}Failures{bold_delimiter}: {roll_result.failures}"
    specials = [f'{italic_delimiter}{special}{italic_delimiter}' for special in _list_specials(roll_result)]
    if specials:
        result += f'\n{list_prefix} {bold_delimiter}Special{bold_delimiter}: ' + \
                  ', '.join(specials)
    return result


def _list_specials(self: RollResult) -> List[str]:
    specials = []
    if self.is_critical:
        specials.append("critical hit")
    if self.is_messy_critical:
        specials.append("messy critical")
    if self.is_bestial_failure:
        specials.append("bestial failure")
    return specials


def _map_to_str(rolls: List[int]) -> str:
    return ' `[' + ', '.join([str(i) for i in rolls]) + ']`'


def _parse(comment: str, comment_delimiter: str = '*') -> str:
    if comment:
        return f" {comment_delimiter}'{comment}'{comment_delimiter}"
    else:
        return ''
