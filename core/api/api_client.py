import os
import time
from typing import Any

import requests
from dotenv import load_dotenv

from core.settings import TOKEN_URL


MAX_RETRIES = 5
DEFAULT_RETRY_DELAY = 3


def load_credentials() -> tuple[str, str]:
    load_dotenv()

    client_id = os.getenv("CLIENT_ID")
    client_secret = os.getenv("CLIENT_SECRET")

    if not client_id:
        raise RuntimeError(
            "Missing CLIENT_ID in .env file."
        )

    if not client_secret:
        raise RuntimeError(
            "Missing CLIENT_SECRET in .env file."
        )

    return client_id, client_secret


def get_access_token(
    client_id: str,
    client_secret: str,
) -> str:
    for attempt in range(MAX_RETRIES):
        response = requests.post(
            TOKEN_URL,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
            },
            timeout=30,
        )

        if response.status_code != 429:
            response.raise_for_status()
            break

        retry_after = response.headers.get(
            "Retry-After"
        )

        delay = (
            int(retry_after)
            if retry_after
            else DEFAULT_RETRY_DELAY * (attempt + 1)
        )

        time.sleep(delay)
    else:
        raise RuntimeError(
            "42 API rate limit exceeded while "
            "requesting an access token."
        )

    data: dict[str, Any] = response.json()
    access_token = data.get("access_token")

    if not isinstance(access_token, str):
        raise RuntimeError(
            "Invalid access token."
        )

    if not access_token:
        raise RuntimeError(
            "Empty access token."
        )

    return access_token


def get_request(
    url: str,
    access_token: str,
    params: dict[str, Any] | None = None,
) -> Any:
    for attempt in range(MAX_RETRIES):
        response = requests.get(
            url,
            headers={
                "Authorization": (
                    f"Bearer {access_token}"
                ),
                "Accept": "application/json",
            },
            params=params,
            timeout=40,
        )

        if response.status_code != 429:
            response.raise_for_status()
            return response.json()

        retry_after = response.headers.get(
            "Retry-After"
        )

        delay = (
            int(retry_after)
            if retry_after
            else DEFAULT_RETRY_DELAY * (attempt + 1)
        )

        print(
            "42 API rate limit reached. "
            f"Retrying in {delay} seconds..."
        )

        time.sleep(delay)

    raise RuntimeError(
        "42 API rate limit exceeded after "
        f"{MAX_RETRIES} attempts."
    )