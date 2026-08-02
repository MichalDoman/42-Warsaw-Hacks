from typing import Any
import time
from typing import Any

from core.api.api_client import (
    get_access_token,
    load_credentials,
)
from core.api.coalitions import get_all_coalition_users
from core.api.locations import (
    get_locations_logged_in_today,
    segregate_locations_by_coalition,
)
from core.api.projects import create_projects_for_warsaw_users
from core.api.users import get_all_users
from core.data_types import Location
from core.services.coalitions_stats import (
    count_unique_users_by_coalition,
    get_leading_coalition,
)
from core.services.projects_stats import (
    get_latest_projects_data,
    get_mission_streak,
)
from core.services.users_stats import (
    get_first_login_today,
    get_top_3_richest_users,
)
from core.services.locations_stats import (
    build_hour_labels,
    get_hourly_login_activity,
    get_peak_login_hour,
)

DASHBOARD_CACHE_TTL = 120

_dashboard_cache: dict[str, Any] | None = None
_dashboard_cache_created_at = 0.0

def load_coalition_presence(
    access_token: str,
    today_locations: list[Location],
) -> dict[str, int]:
    """
    Count unique users who logged in today,
    grouped by coalition.
    """
    coalition_users = get_all_coalition_users(
        access_token
    )

    locations_by_coalition = (
        segregate_locations_by_coalition(
            locations=today_locations,
            coalition_users=coalition_users,
        )
    )

    return count_unique_users_by_coalition(
        locations_by_coalition
    )


def build_coalition_statistics(
    coalition_counts: dict[str, int],
) -> list[dict[str, str | int | float]]:
    """
    Build data for coalition cards.

    Active members use real data.
    Other statistics are temporary mock values.
    """
    return [
        {
            "slug": "orionis",
            "name": "Orionis",
            "average_score": 103.8,
            "active_members": coalition_counts.get(
                "orionis",
                0,
            ),
            "top_10_points": 18_420,
        },
        {
            "slug": "lunaria",
            "name": "Lunaria",
            "average_score": 101.4,
            "active_members": coalition_counts.get(
                "lunaria",
                0,
            ),
            "top_10_points": 16_980,
        },
        {
            "slug": "unitterax",
            "name": "Unitterax",
            "average_score": 105.1,
            "active_members": coalition_counts.get(
                "unitterax",
                0,
            ),
            "top_10_points": 17_750,
        },
    ]


def _load_dashboard_data() -> dict[str, Any]:
    """
    Load and prepare all data required by dashboard.html.
    """
    client_id, client_secret = load_credentials()

    access_token = get_access_token(
        client_id=client_id,
        client_secret=client_secret,
    )

    all_users = get_all_users(
        access_token
    )

    today_locations = get_locations_logged_in_today(
        access_token
    )
    hourly_login_activity = get_hourly_login_activity(
        today_locations
    )

    peak_login_hour = get_peak_login_hour(
        hourly_login_activity
    )

    coalition_counts = load_coalition_presence(
        access_token=access_token,
        today_locations=today_locations,
    )

    leading_coalition, leading_count = (
        get_leading_coalition(
            coalition_counts
        )
    )

    total_logged_in = sum(
        count
        for coalition, count in coalition_counts.items()
        if coalition != "unknown"
    )

    first_login = get_first_login_today(
        locations=today_locations,
        users=all_users,
    )

    all_projects = create_projects_for_warsaw_users(
        users=all_users,
        access_token=access_token,
        days=10,
    )

    richest_users = get_top_3_richest_users(
        all_users
    )

    mission_streak = get_mission_streak(
    all_projects
)

    coalition_statistics = (
        build_coalition_statistics(
            coalition_counts
        )
    )

    return {
        "coalition_counts": coalition_counts,

        "leading_coalition": (
            leading_coalition
            if leading_coalition is not None
            else "none"
        ),

        "leading_count": leading_count,
        "total_logged_in": total_logged_in,
        "first_login": first_login,
        "mission_streak": mission_streak,
        "hourly_login_activity": hourly_login_activity,
        "hour_labels": build_hour_labels(),
        "peak_login_hour": peak_login_hour,
        

        "coalition_statistics": (
            coalition_statistics
        ),

        "richest_users": [
            {
                "login": user.login,
                "wallet": user.wallet,
            }
            for user in richest_users
        ],

        "projects": get_latest_projects_data(
            projects=all_projects,
            users=all_users,
            limit=5,
        ),

        "evaluation_count": 42,
        "top_project": "minishell",
    }

def get_dashboard_data(
    force_refresh: bool = False,
) -> dict[str, Any]:
    global _dashboard_cache
    global _dashboard_cache_created_at

    current_time = time.monotonic()

    cache_is_valid = (
        _dashboard_cache is not None
        and (
            current_time
            - _dashboard_cache_created_at
        )
        < DASHBOARD_CACHE_TTL
    )

    if cache_is_valid and not force_refresh:
        return _dashboard_cache

    dashboard_data = _load_dashboard_data()

    _dashboard_cache = dashboard_data
    _dashboard_cache_created_at = current_time

    return dashboard_data