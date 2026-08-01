from core.api.api_client import get_access_token, load_credentials
from core.api.coalitions import get_all_coalition_users
from core.api.locations import get_all_locations, segregate_locations_by_coalition
from core.api.users import get_all_users

from core.services.users_stats import get_top_3_richest_users
from core.services.projects_stats import get_latest_projects_data


def load_coalition_presence() -> dict[str, int]:
    """Load current campus presence grouped by coalition."""
    client_id, client_secret = load_credentials()
    access_token = get_access_token(client_id, client_secret)

    users = get_all_coalition_users(access_token)
    locations = get_all_locations(access_token)
    segregated_logged_in = segregate_locations_by_coalition(locations, users)

    return {
        "orionis": len(segregated_logged_in.get("orionis", [])),
        "lunaria": len(segregated_logged_in.get("lunaria", [])),
        "unitterax": len(segregated_logged_in.get("unitterax", [])),
        "unknown": len(segregated_logged_in.get("unknown", [])),
    }


def get_dashboard_data() -> dict:
    client_id, client_secret = load_credentials()
    access_token = get_access_token(client_id, client_secret)

    coalition_counts = load_coalition_presence()
    all_users = get_all_users(access_token)
    richest_users = get_top_3_richest_users(all_users)
    known_coalitions = {
        name: count
        for name, count in coalition_counts.items()
        if name != "unknown"
    }

    if known_coalitions:
        leading_coalition = max(known_coalitions, key=known_coalitions.get)
        leading_count = known_coalitions[leading_coalition]
    else:
        leading_coalition = "orionis"
        leading_count = 0

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
        "projects": get_latest_projects_data(all_users, access_token),
        "xp_values": [12, 18, 27, 43, 66, 94, 51],
        "returning_users": ["natalia", "student42", "jnowak"],
        "evaluation_count": 42,
        "top_project": "minishell",
    }