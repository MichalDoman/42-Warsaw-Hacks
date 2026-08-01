from core.data_types import Project


def get_latest_projects(
    projects: list[Project],
    limit: int = 5,
) -> list[Project]:
    sorted_projects = sorted(
        projects,
        key=lambda project: datetime.fromisoformat(
            project.closed_at.replace("Z", "+00:00")
        ),
        reverse=True,
    )

    return sorted_projects[:limit]