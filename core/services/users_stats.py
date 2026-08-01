from core.data_types import User


def get_top_3_richest_users(
    users: list[User],
) -> list[User]:
    return sorted(
        users,
        key=lambda user: user.wallet,
        reverse=True,
    )[:3]