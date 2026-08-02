from core.data_types import Location


def count_unique_users_by_coalition(
    locations_by_coalition: dict[str, list[Location]],
) -> dict[str, int]:
    """
    Count unique users in every coalition.

    A user is counted only once even if they logged in several times.
    """
    result: dict[str, int] = {}

    for coalition_name, locations in locations_by_coalition.items():
        unique_user_ids = {
            location.user_id
            for location in locations
        }

        result[coalition_name] = len(unique_user_ids)

    return result


def get_leading_coalition(
    coalition_counts: dict[str, int],
) -> tuple[str | None, int]:
    """
    Return the coalition with the highest number of users.

    The 'unknown' category is excluded.
    """
    known_coalitions = {
        coalition_name: count
        for coalition_name, count in coalition_counts.items()
        if coalition_name != "unknown"
    }

    if not known_coalitions:
        return None, 0

    leading_coalition = max(
        known_coalitions,
        key=known_coalitions.get,
    )

    return (
        leading_coalition,
        known_coalitions[leading_coalition],
    )