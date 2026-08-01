import os
import sys
from typing import Any

import requests
from dotenv import load_dotenv


TOKEN_URL = "https://api.intra.42.fr/oauth/token"
API_BASE_URL = "https://api.intra.42.fr/v2"


def load_credentials() -> tuple[str, str]:
    load_dotenv()

    client_id = os.getenv("FT_CLIENT_ID")
    client_secret = os.getenv("FT_CLIENT_SECRET")

    if not client_id:
        raise RuntimeError("Brakuje FT_CLIENT_ID w pliku .env.")

    if not client_secret:
        raise RuntimeError("Brakuje FT_CLIENT_SECRET w pliku .env.")

    return client_id, client_secret


def get_access_token(client_id: str, client_secret: str) -> str:
    response = requests.post(
        TOKEN_URL,
        data={
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        },
        timeout=30,
    )

    response.raise_for_status()

    data: dict[str, Any] = response.json()
    access_token = data.get("access_token")

    if not isinstance(access_token, str) or not access_token:
        raise RuntimeError("Odpowiedź nie zawiera poprawnego access tokenu.")

    return access_token


def get_coalition_by_id(
    access_token: str,
    coalition_id: int,
) -> dict[str, Any]:
    response = requests.get(
        f"{API_BASE_URL}/coalitions/{coalition_id}",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
        timeout=15,
    )

    response.raise_for_status()

    data = response.json()

    if not isinstance(data, dict):
        raise RuntimeError(
            "API zwróciło dane koalicji w nieoczekiwanym formacie."
        )

    return data


def main() -> None:
    try:
        client_id, client_secret = load_credentials()
        access_token = get_access_token(client_id, client_secret)

        lunaria = get_coalition_by_id(access_token, 459)
        print(lunaria)

    except requests.Timeout:
        print("Przekroczono czas oczekiwania na odpowiedź 42 API.")
        sys.exit(1)

    except requests.HTTPError as error:
        response = error.response

        if response is None:
            print(f"Wystąpił błąd HTTP: {error}")
        else:
            print(f"42 API zwróciło HTTP {response.status_code}.")
            print(response.text)

        sys.exit(1)

    except requests.RequestException as error:
        print(f"Błąd połączenia z 42 API: {error}")
        sys.exit(1)

    except (RuntimeError, ValueError) as error:
        print(f"Błąd konfiguracji lub danych: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()