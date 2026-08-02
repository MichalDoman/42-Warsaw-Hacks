from datetime import datetime, time
from typing import Any

from core.data_types import Location, User
from core.settings import WARSAW_TIMEZONE


def get_top_3_richest_users(
    users: list[User],
) -> list[User]:
    return sorted(
        users,
        key=lambda user: user.wallet,
        reverse=True,
    )[:3]


def parse_location_datetime(
    location: Location,
) -> datetime:
    return datetime.fromisoformat(
        location.begin_at.replace("Z", "+00:00")
    )


def get_first_login_today(
    locations: list[Location],
    users: list[User],
) -> dict[str, Any] | None:
    """
    Return the first Warsaw student who logged in today.

    The returned time is converted to Europe/Warsaw timezone.
    """
    if not locations:
        return None

    first_location = min(
        locations,
        key=parse_location_datetime,
    )

    users_by_id = {
        user.id: user
        for user in users
    }

    user = users_by_id.get(first_location.user_id)

    if user is None:
        return None

    login_time = parse_location_datetime(
        first_location
    ).astimezone(WARSAW_TIMEZONE)

    return {
        "login": user.login,
        "name": user.name,
        "img_link": user.img_link,
        "time": login_time.strftime("%H:%M"),
        "location": first_location.location,
    }


def get_first_login_after_sunrise(
    locations: list[Location],
    users: list[User],
    sunrise_hour: int = 5,
    sunrise_minute: int = 30,
) -> dict[str, Any] | None:
    """
    Return the first user who logged in today at or after 05:30.

    Login sessions before the configured sunrise time
    are ignored.
    """
    sunrise_time = time(
        hour=sunrise_hour,
        minute=sunrise_minute,
    )

    locations_after_sunrise: list[
        tuple[Location, datetime]
    ] = []

    for location in locations:
        login_datetime = datetime.fromisoformat(
            location.begin_at.replace(
                "Z",
                "+00:00",
            )
        ).astimezone(WARSAW_TIMEZONE)

        if login_datetime.time() >= sunrise_time:
            locations_after_sunrise.append(
                (
                    location,
                    login_datetime,
                )
            )

    if not locations_after_sunrise:
        return None

    first_location, first_login_datetime = min(
        locations_after_sunrise,
        key=lambda item: item[1],
    )

    users_by_id = {
        user.id: user
        for user in users
    }

    user = users_by_id.get(
        first_location.user_id
    )

    if user is None:
        return None

    return {
        "login": user.login,
        "name": user.name,
        "img_link": user.img_link,
        "time": first_login_datetime.strftime(
            "%H:%M"
        ),
        "location": first_location.location,
    }


def get_today_explorers_wallet(
    locations: list[Location],
    users: list[User],
) -> int:
    """
    Return the total wallet balance of all unique users
    who logged in today.
    """
    active_user_ids = {
        location.user_id
        for location in locations
    }

    return sum(
        user.wallet
        for user in users
        if user.id in active_user_ids
    )