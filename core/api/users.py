from typing import Dict, Any, List

import requests

from core.settings import API_BASE_URL, WARSAW_CAMPUS_ID
from core.api.api_client import get_request


def get_active_users(
    access_token: str,
    coalition_id: int,
) -> List[Dict[str, Any]]:
    users = get_request(
        url=f"{API_BASE_URL}/coalitions/{coalition_id}/users",
        access_token=access_token,
        params={
            "page[number]": 1,
            "page[size]": 100,
        },
    )

    return [
        user
        for user in users
        if user.get("active?") is True
    ]


def get_warsaw_locations(
    access_token: str,
) -> List[Dict[str, Any]]:
    return get_request(
        url=f"{API_BASE_URL}/campus/{WARSAW_CAMPUS_ID}/locations",
        access_token=access_token,
        params={
            "page[number]": 1,
            "page[size]": 100,
        },
    )