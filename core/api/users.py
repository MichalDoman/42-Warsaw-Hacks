from typing import Dict, Any, List

from datetime import datetime, date, timedelta, timezone
import time
import requests

from core.settings import (
    COALITIONS_IDS,
    API_BASE_URL,
    WARSAW_CAMPUS_ID,
    WARSAW_TIMEZONE
)
from core.api.api_client import get_request
from core.data_types import User, Location


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
    time.sleep(1)
    lunaria = get_coalition_users(access_token, COALITIONS_IDS["lunaria"])
    time.sleep(1)
    unitterax = get_coalition_users(access_token, COALITIONS_IDS["unitterax"])
    time.sleep(1)

    return {
        "orionis": orionis,
        "lunaria": lunaria,
        "unitterax": unitterax
    }

def create_user(user_data: dict[str, Any]) -> User:
    return User(
        id=user_data["id"],
        login=user_data["login"],
        name=user_data["usual_full_name"],
        img_link=user_data["image"]["link"],
        wallet=user_data["wallet"],
        is_active=user_data["active?"],
    )

def get_all_users(
    access_token: str,
) -> list[User]:
    all_users: list[User] = []

    page_number = 1
    page_size = 100

    while True:
        users_data: list[dict[str, Any]] = get_request(
            url=f"{API_BASE_URL}/campus/{WARSAW_CAMPUS_ID}/users",
            access_token=access_token,
            params={
                "page[number]": 1,
                "page[size]": 100,
                "filter[kind]": "student",
                "filter[staff?]": False
            },
        )

        if not users_data:
            break

        for user_data in users_data:
            all_users.append(create_user(user_data))

        if len(users_data) < page_size:
            break

        page_number += 1

    return all_users


def create_location(
    location_data: dict[str, Any]
) -> Location:
    return Location(
        user_id=location_data["user"]["id"],
        location=location_data["host"],
        begin_at=location_data["begin_at"]
    )


def get_all_locations(
    access_token: str,
) -> list[Location]:
    locations = get_request(
        url=f"{API_BASE_URL}/campus/{WARSAW_CAMPUS_ID}/locations",
        access_token=access_token,
        params={
            "page[number]": 1,
            "page[size]": 100,
        },
    )

    result: list[dict[str, Any]] = []

    for location_data in locations:
        result.append(create_location(location_data))

    return result


def filter_users_logged_in_today(
    users: list[User],
) -> list[User]:
    today = datetime.now(WARSAW_TIMEZONE).date()

    result: list[User] = []

    for user in users:
        login_datetime = datetime.fromisoformat(
            user.begin_at.replace("Z", "+00:00")
        ).astimezone(WARSAW_TIMEZONE)

        if login_datetime.date() == today:
            result.append(user)

    return result


from typing import Any


def segregate_locations_by_coalition(
    locations: list[Location],
    coalition_users: dict[str, list[dict[str, Any]]],
) -> dict[str, list[Location]]:
    locations_by_coalition: dict[str, list[Location]] = {
        coalition_name: []
        for coalition_name in coalition_users
    }

    locations_by_coalition["unknown"] = []

    for location in locations:
        found_coalition = False

        for coalition_name, users in coalition_users.items():
            for user in users:
                if int(user["user_id"]) == int(location.user_id):
                    locations_by_coalition[coalition_name].append(location)
                    found_coalition = True
                    break

            if found_coalition:
                break

        if not found_coalition:
            locations_by_coalition["unknown"].append(location)

    return locations_by_coalition


def get_top_3_richest_users(
    users: list[User],
) -> list[User]:
    return sorted(
        users,
        key=lambda user: user.wallet,
        reverse=True,
    )[:4]


def get_projects_users(
    access_token: str,
    page_size: int = 100,
) -> list[dict[str, Any]]:
    return get_request(
        url=f"{API_BASE_URL}/projects_users",
        access_token=access_token,
        params={
            "page[number]": 1,
            "page[size]": page_size,
            "filter[campus]": 67,
            "filter[staff?]": False
        },
    )