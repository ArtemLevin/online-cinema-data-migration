from dataclasses import dataclass
from uuid import UUID
from dataclasses_post_init_mixin import DataclassesPostInitMixin

@dataclass
class Genre(DataclassesPostInitMixin):
    id: UUID
    name: str
    description: str
    created_at: str
    updated_at: str
