from typing import Any

from core.api.api_client import get_access_token, load_credentials
from core.api.coalitions import get_all_coalition_users
from core.api.locations import (
    get_all_locations,
    segregate_locations_by_coalition,
)
from core.api.projects import create_projects_for_warsaw_users
from core.api.users import get_all_users
from core.services.projects_stats import get_latest_projects_data
from core.services.users_stats import get_top_3_richest_users


def load_coalition_presence(
    access_token: str,
) -> dict[str, int]:
    coalition_users = get_all_coalition_users(access_token)
    locations = get_all_locations(access_token)

    segregated_logged_in = segregate_locations_by_coalition(
        locations,
        coalition_users,
    )

    return {
        "orionis": len(
            segregated_logged_in.get("orionis", [])
        ),
        "lunaria": len(
            segregated_logged_in.get("lunaria", [])
        ),
        "unitterax": len(
            segregated_logged_in.get("unitterax", [])
        ),
        "unknown": len(
            segregated_logged_in.get("unknown", [])
        ),
    }


def get_dashboard_data() -> dict[str, Any]:
    client_id, client_secret = load_credentials()

    access_token = get_access_token(
        client_id=client_id,
        client_secret=client_secret,
    )

    all_users = get_all_users(access_token)

    all_projects = create_projects_for_warsaw_users(
        users=all_users,
        access_token=access_token,
    )

    coalition_counts = load_coalition_presence(
        access_token=access_token,
    )

    known_coalitions = {
        name: count
        for name, count in coalition_counts.items()
        if name != "unknown"
    }

    if known_coalitions:
        leading_coalition = max(
            known_coalitions,
            key=known_coalitions.get,
        )
        leading_count = known_coalitions[leading_coalition]
    else:
        leading_coalition = "orionis"
        leading_count = 0

    richest_users = get_top_3_richest_users(all_users)

    return {
        "coalition_counts": coalition_counts,
        "leading_coalition": leading_coalition,
        "leading_count": leading_count,
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
        ),
        "xp_values": [12, 18, 27, 43, 66, 94, 51],
        "returning_users": [
            "natalia",
            "student42",
            "jnowak",
        ],
        "evaluation_count": 42,
        "top_project": "minishell",
    }
