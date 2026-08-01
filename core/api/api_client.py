import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv

from core.settings import TOKEN_URL


def load_credentials() -> tuple[str, str]:
    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id:
        raise RuntimeError("Missing CLIENT_ID in .env file.")

    if not client_secret:
        raise RuntimeError("Missing CLIENT_SECRET in .env file.")

    return client_id, client_secret


def get_access_token(client_id: str, client_secret: str) -> str:
    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )

    response.raise_for_status()

    data: dict[str, Any] = response.json()
    access_token = data.get("access_token")

    if not isinstance(access_token, str) or not access_token:
        raise RuntimeError("Invalid access token.")

    return access_token


def get_request(
    url: str,
    access_token: str,
    params: dict[str, Any] | None = None,
) -> Any:
    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
        params=params,
        timeout=40,
    )

    response.raise_for_status()

    return response.json()

