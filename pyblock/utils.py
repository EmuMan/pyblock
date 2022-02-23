import io
import base64

import requests
from nbt import nbt

from .errors import *
from .errors import _get_response_exception

def decode_item_bytes(item_bytes: bytes) -> nbt.NBTFile:
    return nbt.NBTFile(fileobj=io.BytesIO(base64.b64decode(item_bytes)))

def request_endpoint(endpoint: str, args: dict[str, str] | None = None) -> dict:
    valid_args = {item[0]: item[1] for item in args.items()} if args is not None else {}
    url = f'https://api.hypixel.net/{endpoint}'
    response = requests.get(url, params=valid_args)
    if not response.ok: raise HTTPInvalidResponse(response)
    if error := _get_response_exception(response) is not None:
        raise error
    return response.json()
