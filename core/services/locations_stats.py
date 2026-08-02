from datetime import datetime

from core.data_types import Location
from core.settings import WARSAW_TIMEZONE


def parse_location_datetime(
    location: Location,
) -> datetime:
    return datetime.fromisoformat(
        location.begin_at.replace("Z", "+00:00")
    ).astimezone(WARSAW_TIMEZONE)


def get_hourly_login_activity(
    locations: list[Location],
) -> list[int]:
    """
    Count unique users who logged in during every hour today.

    Index 0 represents 00:00-00:59.
    Index 23 represents 23:00-23:59.
    """
    users_by_hour: dict[int, set[int]] = {
        hour: set()
        for hour in range(24)
    }

    for location in locations:
        login_datetime = parse_location_datetime(location)
        login_hour = login_datetime.hour

        users_by_hour[login_hour].add(
            location.user_id
        )

    return [
        len(users_by_hour[hour])
        for hour in range(24)
    ]


def get_peak_login_hour(
    hourly_activity: list[int],
) -> dict[str, str | int] | None:
    """
    Return the hour with the highest login activity.

    If several hours have the same result, the earliest
    one is selected.
    """
    if not hourly_activity:
        return None

    peak_count = max(hourly_activity)

    if peak_count == 0:
        return None

    peak_hour = hourly_activity.index(peak_count)
    next_hour = (peak_hour + 1) % 24

    return {
        "hour": peak_hour,
        "count": peak_count,
        "label": (
            f"{peak_hour:02d}:00–"
            f"{next_hour:02d}:00"
        ),
    }


def build_hour_labels() -> list[str]:
    return [
        f"{hour:02d}:00"
        for hour in range(24)
    ]