from dataclasses import dataclass

@dataclass
class User:
	id: int
	login: str
	name: str
	location: str
	img_link: str
	wallet: int
	updated_at: str
	is_active: bool