from typing import Dict, Any, List

from datetime import datetime, date, timedelta, timezone
import requests

from core.settings import API_BASE_URL, WARSAW_CAMPUS_ID, WARSAW_TIMEZONE
from core.api.api_client import get_request
from core.data_types import User


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


def create_user(location_data: dict[str, Any]) -> User:
    user_data = location_data["user"]

    return User(
        id=user_data["id"],
        login=user_data["login"],
        name=user_data["usual_full_name"],
        location=location_data["host"],
        img_link=user_data["image"]["link"],
        wallet=user_data["wallet"],
        updated_at=user_data["updated_at"],
        is_active=user_data["active?"],
    )


def get_users_logged_in_today(
    access_token: str,
) -> list[dict[str, Any]]:
    users = get_request(
        url=f"{API_BASE_URL}/campus/{WARSAW_CAMPUS_ID}/locations",
        access_token=access_token,
        params={
            "page[number]": 1,
            "page[size]": 100,
        },
    )

    today = datetime.now(WARSAW_TIMEZONE).date()
    result: list[dict[str, Any]] = []

    for user in users:
        user_section = user.get("user", {})
        updated_at = user_section.get("updated_at")

        if not updated_at:
            continue

        updated_datetime = datetime.fromisoformat(
            updated_at.replace("Z", "+00:00")
        ).astimezone(WARSAW_TIMEZONE)

        if updated_datetime.date() == today:
            result.append(create_user(user))

    return result
