from dataclasses import dataclass
from uuid import UUID
from dataclasses_post_init_mixin import DataclassesPostInitMixin


@dataclass
class FilmWork(DataclassesPostInitMixin):
    id: UUID
    title: str
    description: str
    creation_date: str
    file_path: str
    rating: float
    type: str
    created_at: str
    updated_at: str


