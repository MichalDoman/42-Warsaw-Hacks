from typing import Dict, Any, List

from datetime import datetime, date, timedelta, timezone
import time
import requests

from core.settings import (
    API_BASE_URL,
    WARSAW_CAMPUS_ID,
    WARSAW_TIMEZONE
)
from core.api.api_client import get_request
from core.data_types import User, Project


def get_active_warsaw_user_ids(
    users: list[User],
) -> set[int]:
    return {
        user.id
        for user in users
        if user.is_active
    }


def create_projects_for_warsaw_users(
    projects_users: list[dict[str, Any]],
    warsaw_user_ids: set[int],
) -> list[Project]:
    projects: list[Project] = []

    for project_user in projects_users:
        user_data = project_user.get("user", {})
        project_data = project_user.get("project", {})

        user_id = user_data.get("id")

        if user_id is None:
            continue

        if int(user_id) not in warsaw_user_ids:
            continue

        project_id = project_data.get("id")
        project_name = project_data.get("name")
        closed_at = project_user.get("marked_at")

        if project_id is None or project_name is None or closed_at is None:
            continue

        projects.append(
            Project(
                id=int(project_id),
                user_id=int(user_id),
                name=str(project_name),
                final_mark=project_user.get("final_mark"),
                closed_at=str(closed_at),
                status=str(project_user.get("status", "")),
            )
        )

    return projects


def get_projects_users(
    access_token: str,
) -> list[dict[str, Any]]:
    all_projects_users: list[dict[str, Any]] = []

    now = datetime.now(timezone.utc)
    three_days_ago = now - timedelta(days=3)

    page_number = 1
    page_size = 100

    while True:
        projects_users: list[dict[str, Any]] = get_request(
            url=f"{API_BASE_URL}/projects_users",
            access_token=access_token,
            params={
                "page[number]": page_number,
                "page[size]": page_size,
                "filter[status]": "finished",
                "range[marked_at]": (
                    f"{three_days_ago.isoformat()},"
                    f"{now.isoformat()}"
                ),
            },
        )

        if not projects_users:
            break

        all_projects_users.extend(projects_users)

        if len(projects_users) < page_size:
            break

        page_number += 1

    return all_projects_users
