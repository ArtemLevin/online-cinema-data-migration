from dataclasses import dataclass
from uuid import UUID
from dataclasses_post_init_mixin import DataclassesPostInitMixin

@dataclass
class PersonFilmWork(DataclassesPostInitMixin):
    id: UUID
    person_id: UUID
    film_work_id: UUID
    role: str
    created_at: str

