import requests

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