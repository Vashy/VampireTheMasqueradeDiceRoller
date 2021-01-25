import os
from typing import Final

COMMAND_PREFIX = None
TOKEN_API_KEY: Final = 'VTM_BOT_TOKEN'


def invoking_command_prefix(prefix=COMMAND_PREFIX) -> str:
    return prefix + 'r'


def without_command_prefix(content: str, prefix=COMMAND_PREFIX) -> str:
    return content.lstrip(invoking_command_prefix(prefix))


def get_api_token() -> str:
    token = os.getenv(TOKEN_API_KEY)
    if not token:
        print(f'please provide a {TOKEN_API_KEY} environment variable')
        exit(1)

    return token
