import os
import sys
import time
from typing import Any

import requests

from core.settings import COALITIONS_IDS
from core.api.api_client import load_credentials, get_access_token
from core.api.coalitions import get_coalition_by_id, get_coalition_users
from core.api.users import get_active_users, get_users_logged_in_today, get_finished_projects_this_week


def main() -> None:
    try:
        client_id, client_secret = load_credentials()
        access_token = get_access_token(client_id, client_secret)

        # orionis = get_coalition_by_id(access_token, COALITIONS_IDS["orionis"])
        # time.sleep(1)
        # lunaria = get_coalition_by_id(access_token, COALITIONS_IDS["lunaria"])
        # time.sleep(1)
        # unitterax = get_coalition_by_id(access_token, COALITIONS_IDS["unitterax"])
        # time.sleep(1)

        # print(orionis)
        # print(lunaria)
        # print(unitterax)
        # print()

        # lunaria_users = get_coalition_users(access_token, COALITIONS_IDS["lunaria"])
        # print(lunaria_users)

        # lunaria_active_users = get_active_users(access_token, COALITIONS_IDS["lunaria"])
        # for item in lunaria_active_users:
        #     print(item)

        # users_logged_in_today = get_users_logged_in_today(access_token)
        # print(users_logged_in_today)

        finished_projects_this_week = get_finished_projects_this_week(access_token)
        print(finished_projects_this_week)

    except requests.Timeout:
        print("42 API response timeout.")
        sys.exit(1)

    except requests.HTTPError as error:
        response = error.response

        if response is None:
            print(f"HTTP Error: {error}")
        else:
            print(f"42 API response status code: {response.status_code}.")
            print(response.text)

        sys.exit(1)

    except requests.RequestException as error:
        print(f"Error connectiong 42 API: {error}")
        sys.exit(1)

    except (RuntimeError, ValueError) as error:
        print(f"Configuration error: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()