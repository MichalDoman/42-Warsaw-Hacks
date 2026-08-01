from typing import Dict, Any

import requests

from core.settings import API_BASE_URL
from core.api.api_client import get_request


def get_coalition_by_id(
    access_token: str,
    coalition_id: int,
) -> Dict[str, Any]:
    data = get_request(
        url=f"{API_BASE_URL}/coalitions/{coalition_id}",
        access_token=access_token,
        params={
            "page[number]": 1,
            "page[size]": 100,
        },
    )

    if not isinstance(data, dict):
        raise RuntimeError("Invalid data format.")

    return data


def get_coalition_users(
	access_token: str,
	coalition_id: int
) -> Dict[str, Any]:
	data = get_request(
        url=f"{API_BASE_URL}/coalitions/{coalition_id}/coalitions_users",
        access_token=access_token,
        params={
            "page[number]": 1,
            "page[size]": 100,
        },
    )

	return data
    