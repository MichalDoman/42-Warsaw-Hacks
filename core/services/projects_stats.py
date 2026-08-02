from datetime import datetime, timedelta

from core.data_types import Project, User
from core.settings import WARSAW_TIMEZONE


def parse_project_date(
    project: Project,
) -> datetime:
    return datetime.fromisoformat(
        project.closed_at.replace("Z", "+00:00")
    )


def get_latest_projects(
    projects: list[Project],
    limit: int = 5,
) -> list[Project]:
    passed_projects = [
        project
        for project in projects
        if project.validated
    ]

    return sorted(
        passed_projects,
        key=parse_project_date,
        reverse=True,
    )[:limit]


def get_latest_projects_data(
    projects: list[Project],
    users: list[User],
    limit: int = 5,
) -> list[dict[str, str | int | None]]:
    users_by_id = {
        user.id: user
        for user in users
    }

    latest_projects = get_latest_projects(
        projects=projects,
        limit=limit,
    )

    result: list[dict[str, str | int | None]] = []

    for project in latest_projects:
        user = users_by_id.get(project.user_id)

        if user is None:
            continue

        result.append({
            "login": user.login,
            "img_link": user.img_link,
            "project": project.name,
            "score": project.final_mark,
        })

    return result


def get_project_local_date(
    project: Project,
):
    return (
        parse_project_date(project)
        .astimezone(WARSAW_TIMEZONE)
        .date()
    )


def get_mission_streak(
    projects: list[Project],
) -> int:
    """
    Count consecutive successful projects.

    Rules:
    - Every validated project adds 1 to the streak.
    - Every failed project resets the streak to 0.
    - Projects are processed chronologically.
    """
    sorted_projects = sorted(
        projects,
        key=parse_project_date,
    )

    streak = 0

    for project in sorted_projects:
        if project.validated:
            streak += 1
        else:
            streak = 0

    return streak