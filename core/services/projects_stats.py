from datetime import datetime

from core.data_types import Project, User


def parse_project_date(project: Project) -> datetime:
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
        if project.final_mark is not None
        and project.final_mark >= 100
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