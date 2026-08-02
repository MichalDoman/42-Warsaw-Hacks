from datetime import datetime
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