import os
import sys
from typing import Any

import requests

from core.api.api_client import load_credentials, get_access_token
from core.api.coalitions import get_coalition_by_id, get_coalition_users
from core.api.users import get_all_coalition_users, get_all_users, filter_users_logged_in_today, get_top_3_richest_users, get_all_locations, segregate_locations_by_coalition


def main() -> None:
    try:
        client_id, client_secret = load_credentials()
        access_token = get_access_token(client_id, client_secret)

        all_users = get_all_users(access_token)
        # print(all_users)
        # print()

        # users_logged_in_today = filter_users_logged_in_today(all_users)
        # print(users_logged_in_today)

        # print(get_top_3_richest_users(all_users))

        users = get_all_coalition_users(access_token)
        segregated_logged_in = segregate_locations_by_coalition(
            get_all_locations(access_token),
            users
        )

        print(f"orionis: {len(segregated_logged_in["orionis"])}")
        print(f"lunaria: {len(segregated_logged_in["lunaria"])}")
        print(f"unitterax: {len(segregated_logged_in["unitterax"])}")
        print(f"unknown: {len(segregated_logged_in["unknown"])}")


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