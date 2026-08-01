from core.data_types import Project
from core.api.projects import get_projects_users

from core.data_types import User


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


def get_latest_projects_data(
	users: list[User],
	access_token: str,
	limit: int = 5,
) -> list[dict[str, str | int]]:
	users_by_id = {user.id: user for user in users}

	latest_projects = get_latest_projects(
		projects=get_projects_users(access_token),
		limit=limit,
	)

	result: list[dict[str, str | int]] = []

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