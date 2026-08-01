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
from core.data_types import User, Location, Project


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