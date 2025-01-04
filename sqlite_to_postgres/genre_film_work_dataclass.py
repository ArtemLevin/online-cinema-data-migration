from dataclasses import dataclass
from uuid import UUID
from dataclasses_post_init_mixin import DataclassesPostInitMixin

@dataclass
class GenreFilmWork(DataclassesPostInitMixin):
    id: UUID
    genre_id: UUID
    film_work_id: UUID
    created_at: str

