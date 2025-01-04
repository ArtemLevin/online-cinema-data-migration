from dataclasses import dataclass
from uuid import UUID
from dataclasses_post_init_mixin import DataclassesPostInitMixin

@dataclass
class Person(DataclassesPostInitMixin):
    id: UUID
    full_name: str
    created_at: str
    updated_at: str
