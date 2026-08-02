from typing import Dict, Any, List

import requests
import time

from core.settings import API_BASE_URL, COALITIONS_IDS
from core.api.api_client import get_request


def get_coalition_users(
    access_token: str,
    coalition_id: int,
) -> list[dict[str, Any]]:
    all_users: list[dict[str, Any]] = []

    page_number = 1
    page_size = 100

    while True:
        users = get_request(
            url=f"{API_BASE_URL}/coalitions/{coalition_id}/coalitions_users",
            access_token=access_token,
            params={
                "page[number]": page_number,
                "page[size]": page_size,
            },
        )

        if not users:
            break

        all_users.extend(users)

        if len(users) < page_size:
            break

        page_number += 1

    return all_users


def get_all_coalition_users(
    access_token: str,
) -> Dict[str, List[Dict[str, Any]]]:
    orionis = get_coalition_users(access_token, COALITIONS_IDS["orionis"])
    #time.sleep(1)
    lunaria = get_coalition_users(access_token, COALITIONS_IDS["lunaria"])
    #time.sleep(1)
    unitterax = get_coalition_users(access_token, COALITIONS_IDS["unitterax"])
    #time.sleep(1)

    return {
        "orionis": orionis,
        "lunaria": lunaria,
        "unitterax": unitterax
    }
    