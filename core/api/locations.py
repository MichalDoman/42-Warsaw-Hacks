from datetime import datetime, time, timezone
from typing import Any

from core.api.api_client import get_request
from core.data_types import Location
from core.settings import (
    API_BASE_URL,
    WARSAW_CAMPUS_ID,
    WARSAW_TIMEZONE,
)


def create_location(
    location_data: dict[str, Any],
) -> Location:
    return Location(
        user_id=int(location_data["user"]["id"]),
        location=str(location_data["host"]),
        begin_at=str(location_data["begin_at"]),
    )


def _format_api_datetime(value: datetime) -> str:
    """
    Convert a datetime to the UTC ISO format expected by 42 API.
    """
    return (
        value.astimezone(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def get_today_boundaries_utc() -> tuple[datetime, datetime]:
    """
    Return the beginning and end of the current Warsaw day in UTC.
    """
    today = datetime.now(WARSAW_TIMEZONE).date()

    day_start_local = datetime.combine(
        today,
        time.min,
        tzinfo=WARSAW_TIMEZONE,
    )

    day_end_local = datetime.combine(
        today,
        time.max,
        tzinfo=WARSAW_TIMEZONE,
    )

    return (
        day_start_local.astimezone(timezone.utc),
        day_end_local.astimezone(timezone.utc),
    )


def get_locations_logged_in_today(
    access_token: str,
) -> list[Location]:
    """
    Return all location sessions which started today in Warsaw time.

    All API pages are downloaded.
    """
    day_start_utc, day_end_utc = get_today_boundaries_utc()

    all_locations: list[Location] = []

    page_number = 1
    page_size = 100

    while True:
        locations_data: list[dict[str, Any]] = get_request(
            url=(
                f"{API_BASE_URL}/campus/"
                f"{WARSAW_CAMPUS_ID}/locations"
            ),
            access_token=access_token,
            params={
                "page[number]": page_number,
                "page[size]": page_size,
                "range[begin_at]": (
                    f"{_format_api_datetime(day_start_utc)},"
                    f"{_format_api_datetime(day_end_utc)}"
                ),
                "sort": "begin_at",
            },
        )

        if not locations_data:
            break

        all_locations.extend(
            create_location(location_data)
            for location_data in locations_data
        )

        if len(locations_data) < page_size:
            break

        page_number += 1

    return all_locations


def segregate_locations_by_coalition(
    locations: list[Location],
    coalition_users: dict[str, list[dict[str, Any]]],
) -> dict[str, list[Location]]:
    """
    Group location records by coalition.

    A lookup dictionary is used instead of nested loops.
    """
    user_to_coalition: dict[int, str] = {}

    for coalition_name, users in coalition_users.items():
        for user in users:
            user_id = user.get("user_id")

            if user_id is not None:
                user_to_coalition[int(user_id)] = coalition_name

    locations_by_coalition: dict[str, list[Location]] = {
        coalition_name: []
        for coalition_name in coalition_users
    }

    locations_by_coalition["unknown"] = []

    for location in locations:
        coalition_name = user_to_coalition.get(
            location.user_id,
            "unknown",
        )

        locations_by_coalition[coalition_name].append(location)

    return locations_by_coalition