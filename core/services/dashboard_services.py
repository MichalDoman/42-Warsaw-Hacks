import time
from typing import Any

from core.api.api_client import (
    get_access_token,
    load_credentials,
)
from core.api.coalitions import (
    get_all_coalition_users,
    get_all_coalitions
)
from core.api.locations import (
    get_locations_logged_in_today,
    segregate_locations_by_coalition,
)
from core.api.projects import create_projects_for_warsaw_users
from core.api.users import get_all_users
from core.data_types import Location, Coalition
from core.services.coalitions_stats import (
    count_unique_users_by_coalition,
    get_leading_coalition,
    build_coalition_metrics
)
from core.services.projects_stats import (
    get_latest_projects_data,
    get_mission_streak,
)
from core.services.users_stats import (
    get_first_login_after_sunrise,
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
    today_locations: list[Location],
    coalition_users: dict[str, list[dict[str, Any]]],
) -> dict[str, int]:
    """
    Count unique users who logged in today,
    grouped by coalition.
    """
    locations_by_coalition = segregate_locations_by_coalition(
        locations=today_locations,
        coalition_users=coalition_users,
    )

    return count_unique_users_by_coalition(
        locations_by_coalition
    )


def build_coalition_statistics(
    coalitions: list[Coalition],
    coalition_counts: dict[str, int],
    coalition_metrics: dict[
        str,
        dict[str, int | float],
    ],
) -> list[dict[str, str | int | float]]:
    statistics: list[dict[str, str | int | float]] = []

    for coalition in coalitions:
        slug = coalition.name.lower()
        metrics = coalition_metrics.get(slug, {})

        statistics.append({
            "slug": slug,
            "name": coalition.name,
            "image_url": coalition.image_url,
            "color": coalition.color,
            "total_score": coalition.score,
            "logged_in_today": coalition_counts.get(
                slug,
                0,
            ),
            "active_students": metrics.get(
                "active_students",
                0,
            ),
            "average_score": metrics.get(
                "average_score",
                0.0,
            ),
            "top_10_score": metrics.get(
                "top_10_score",
                0,
            ),
            "top_3_score": metrics.get(
                "top_3_score",
                0,
            ),
        })

    return sorted(
        statistics,
        key=lambda coalition: coalition["total_score"],
        reverse=True,
    )


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

    coalition_users = get_all_coalition_users(
        access_token
    )

    coalition_counts = load_coalition_presence(
        today_locations=today_locations,
        coalition_users=coalition_users,
    )

    leading_coalition, leading_count = get_leading_coalition(
        coalition_counts
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

    first_sunray = get_first_login_after_sunrise(
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

    coalitions = get_all_coalitions(
        access_token
    )

    coalition_metrics = build_coalition_metrics(
        all_coalition_users=coalition_users,
    )

    coalition_statistics = build_coalition_statistics(
        coalitions=coalitions,
        coalition_counts=coalition_counts,
        coalition_metrics=coalition_metrics,
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
        "first_sunray": first_sunray,
        "mission_streak": mission_streak,
        "hourly_login_activity": hourly_login_activity,
        "hour_labels": build_hour_labels(),
        "peak_login_hour": peak_login_hour,
        "coalition_statistics": coalition_statistics,
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