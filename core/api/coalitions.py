from typing import Any
import time

from core.api.api_client import get_request
from core.data_types import Coalition
from core.settings import API_BASE_URL, COALITIONS_IDS


def get_coalition(
    access_token: str,
    coalition_id: int,
) -> dict[str, Any]:
    return get_request(
        url=f"{API_BASE_URL}/coalitions/{coalition_id}",
        access_token=access_token,
    )


def create_coalition(
    coalition_data: dict[str, Any],
) -> Coalition:
    return Coalition(
        id=int(coalition_data["id"]),
        name=str(coalition_data["name"]),
        image_url=str(coalition_data.get("image_url") or ""),
        color=str(coalition_data.get("color") or ""),
        score=int(coalition_data.get("score") or 0),
    )


def get_all_coalitions(
    access_token: str,
) -> list[Coalition]:
    coalitions: list[Coalition] = []

    for index, coalition_id in enumerate(COALITIONS_IDS.values()):
        coalition_data = get_coalition(
            access_token=access_token,
            coalition_id=coalition_id,
        )

        coalitions.append(
            create_coalition(coalition_data)
        )

        if index < len(COALITIONS_IDS) - 1:
            time.sleep(1)

    return coalitions


def get_coalition_users(
    access_token: str,
    coalition_id: int,
) -> list[dict[str, Any]]:
    all_users: list[dict[str, Any]] = []

    page_number = 1
    page_size = 100

    while True:
        users: list[dict[str, Any]] = get_request(
            url=(
                f"{API_BASE_URL}/coalitions/"
                f"{coalition_id}/coalitions_users"
            ),
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
) -> dict[str, list[dict[str, Any]]]:
    coalition_users: dict[str, list[dict[str, Any]]] = {}

    for index, (coalition_name, coalition_id) in enumerate(
        COALITIONS_IDS.items()
    ):
        coalition_users[coalition_name] = get_coalition_users(
            access_token=access_token,
            coalition_id=coalition_id,
        )

        if index < len(COALITIONS_IDS) - 1:
            time.sleep(1)

    return coalition_users
