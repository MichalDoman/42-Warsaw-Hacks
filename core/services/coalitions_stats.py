from typing import Any

from core.data_types import Location


def count_unique_users_by_coalition(
    locations_by_coalition: dict[str, list[Location]],
) -> dict[str, int]:
    """
    Count unique users who logged in today in every coalition.

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
    Return the coalition with the highest number of users logged in today.

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


def get_active_students_count(
    coalition_users: list[dict[str, Any]],
) -> int:
    """
    Count active students in a coalition.
    """
    return sum(
        1
        for coalition_user in coalition_users
        if (coalition_user.get("user") or {}).get("active?") is True
    )


def get_coalition_scores(
    coalition_users: list[dict[str, Any]],
) -> list[int]:
    """
    Return valid coalition scores for all users.
    """
    scores: list[int] = []

    for coalition_user in coalition_users:
        score = coalition_user.get("score")

        if score is None:
            continue

        try:
            scores.append(int(score))
        except (TypeError, ValueError):
            continue

    return scores


def get_average_score_per_user(
    coalition_users: list[dict[str, Any]],
) -> float:
    """
    Calculate the average coalition score per user.
    """
    scores = get_coalition_scores(coalition_users)

    if not scores:
        return 0.0

    return round(
        sum(scores) / len(scores),
        2,
    )


def get_top_users_score_sum(
    coalition_users: list[dict[str, Any]],
    limit: int,
) -> int:
    """
    Return the sum of scores of the top N coalition members.
    """
    scores = sorted(
        get_coalition_scores(coalition_users),
        reverse=True,
    )

    return sum(scores[:limit])


def get_top_10_score_sum(
    coalition_users: list[dict[str, Any]],
) -> int:
    return get_top_users_score_sum(
        coalition_users=coalition_users,
        limit=10,
    )


def get_top_3_score_sum(
    coalition_users: list[dict[str, Any]],
) -> int:
    return get_top_users_score_sum(
        coalition_users=coalition_users,
        limit=3,
    )


def build_coalition_metrics(
    all_coalition_users: dict[str, list[dict[str, Any]]],
) -> dict[str, dict[str, int | float]]:
    """
    Build statistics for every coalition.
    """
    result: dict[str, dict[str, int | float]] = {}

    for coalition_name, coalition_users in all_coalition_users.items():
        result[coalition_name] = {
            "active_students": get_active_students_count(
                coalition_users
            ),
            "average_score": get_average_score_per_user(
                coalition_users
            ),
            "top_10_score": get_top_10_score_sum(
                coalition_users
            ),
            "top_3_score": get_top_3_score_sum(
                coalition_users
            ),
        }

    return result