from dataclasses import dataclass

@dataclass
class User:
	id: int
	login: str
	name: str
	img_link: str
	wallet: int
	is_active: bool


@dataclass
class Location:
	user_id: int
	location: str
	begin_at: str


@dataclass
class Project:
	id: int
	user_id: int
	name: str
	final_mark: int
	closed_at: str
	status: str
