import requests
from flask import Flask, jsonify, render_template

from core.api.api_client import get_access_token, load_credentials
from core.api.users import (
    get_all_users,
    get_all_coalition_users,
    get_all_locations,
    get_top_3_richest_users,
    segregate_locations_by_coalition,
)

app = Flask(__name__)


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
    coalition_counts = load_coalition_presence()
    client_id, client_secret = load_credentials()
    access_token = get_access_token(client_id, client_secret)
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
        "projects": [
            {"login": "natalia", "project": "minishell", "score": 110},
            {"login": "student42", "project": "push_swap", "score": 100},
            {"login": "jnowak", "project": "philosophers", "score": 125},
            {"login": "akowalski", "project": "cub3d", "score": 105},
            {"login": "mnowak", "project": "netpractice", "score": 100},
        ],
        "xp_values": [12, 18, 27, 43, 66, 94, 51],
        "returning_users": ["natalia", "student42", "jnowak"],
        "evaluation_count": 42,
        "top_project": "minishell",
    }


@app.route("/")
def dashboard():
    try:
        return render_template(
            "dashboard.html",
            dashboard=get_dashboard_data(),
            error_message=None,
        )
    except requests.Timeout:
        return render_template(
            "dashboard.html",
            dashboard=None,
            error_message="42 API response timeout.",
        ), 504
    except requests.HTTPError as error:
        response = error.response
        message = (
            f"HTTP error: {error}"
            if response is None
            else f"42 API response status code: {response.status_code}. {response.text}"
        )
        return render_template(
            "dashboard.html",
            dashboard=None,
            error_message=message,
        ), 502
    except requests.RequestException as error:
        return render_template(
            "dashboard.html",
            dashboard=None,
            error_message=f"Error connecting to 42 API: {error}",
        ), 502
    except (RuntimeError, ValueError) as error:
        return render_template(
            "dashboard.html",
            dashboard=None,
            error_message=f"Configuration error: {error}",
        ), 500


@app.route("/api/dashboard")
def dashboard_api():
    try:
        return jsonify(get_dashboard_data())
    except requests.RequestException as error:
        return jsonify({"error": str(error)}), 502
    except (RuntimeError, ValueError) as error:
        return jsonify({"error": str(error)}), 500


def main() -> None:
    app.run(host="127.0.0.1", port=5000, debug=True)


if __name__ == "__main__":
    main()
