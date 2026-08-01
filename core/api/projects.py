from datetime import datetime, timedelta, timezone
from typing import Any

from core.api.api_client import get_request
from core.data_types import Project, User
from core.settings import API_BASE_URL, WARSAW_CAMPUS_ID


def get_active_warsaw_student_ids(
    users: list[User],
) -> set[int]:
    return {
        user.id
        for user in users
        if user.is_active
    }


def get_projects_users(
    access_token: str,
    days: int = 3,
) -> list[dict[str, Any]]:
    all_projects_users: list[dict[str, Any]] = []

    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=days)

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
                "filter[campus]": WARSAW_CAMPUS_ID,
                "range[marked_at]": (
                    f"{start_date.isoformat()},"
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


def create_project(
    project_user: dict[str, Any],
) -> Project | None:
    user_data = project_user.get("user") or {}
    project_data = project_user.get("project") or {}

    user_id = user_data.get("id")
    project_id = project_data.get("id")
    project_name = project_data.get("name")
    final_mark = project_user.get("final_mark")
    marked_at = project_user.get("marked_at")
    status = project_user.get("status")

    if (
        user_id is None
        or project_id is None
        or project_name is None
        or marked_at is None
    ):
        return None

    return Project(
        id=int(project_id),
        user_id=int(user_id),
        name=str(project_name),
        final_mark=(
            int(final_mark)
            if final_mark is not None
            else None
        ),
        closed_at=str(marked_at),
        status=str(status or ""),
    )


def create_projects_for_warsaw_users(
    users: list[User],
    access_token: str,
    days: int = 3,
) -> list[Project]:
    warsaw_student_ids = get_active_warsaw_student_ids(users)

    projects_users = get_projects_users(
        access_token=access_token,
        days=days,
    )

    projects: list[Project] = []

    for project_user in projects_users:
        project = create_project(project_user)

        if project is None:
            continue

        if project.user_id not in warsaw_student_ids:
            continue

        projects.append(project)

    return projects
