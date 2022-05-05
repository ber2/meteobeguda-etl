from typing import Optional

import requests

BASE_URL = "http://www.meteobeguda.cat/download"
URL_TWO_DAYS = f"{BASE_URL}/downld02.txt"
URL_EIGHT_DAYS = f"{BASE_URL}/downld08.txt"


def _get_data(url: str) -> Optional[bytes]:
    response = requests.get(url)
    if response.status_code != 200:
        return None
    return response.content


def get_last_two_days() -> Optional[bytes]:
    return _get_data(URL_TWO_DAYS)


def get_last_eight_days() -> Optional[bytes]:
    return _get_data(URL_EIGHT_DAYS)
