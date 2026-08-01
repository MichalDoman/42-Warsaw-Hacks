from typing import Dict, Any, List

from datetime import datetime, date, timedelta, timezone
import time
import requests

from core.settings import (
    API_BASE_URL,
    WARSAW_CAMPUS_ID,
)
from core.api.api_client import get_request
from core.data_types import User, Project


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
                "page[number]": page_number,
                "page[size]": page_size,
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
