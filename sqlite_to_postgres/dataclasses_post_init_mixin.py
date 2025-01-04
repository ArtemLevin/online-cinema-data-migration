from datetime import datetime
from uuid import UUID
from typing import Any


class DataclassesPostInitMixin:
    # Метод для проверки UUID
    def _validate_uuid(self, id: Any) -> None:
        """
        Проверяет корректность значения UUID.

        :param id: Значение, которое нужно проверить (строка или UUID).
        :raises ValueError: Если значение пустое или имеет некорректный формат.
        """
        if not id:
            raise ValueError("id cannot be null or empty")
        if isinstance(id, str):
            try:
                id = UUID(id)  # Пробуем преобразовать строку в UUID
            except ValueError:
                raise ValueError(f"Invalid UUID format for id: {id}")

    # Метод __post_init__, который будет выполняться после инициализации dataclass
    def __post_init__(self) -> None:
        """
        Выполняет пост-обработку полей dataclass:
        - Проверяет поле UUID.
        - Преобразует `rating` в float, если это необходимо.
        - Преобразует `created_at` и `updated_at` в datetime, если это необходимо.
        """
        # Проверяем все поля, определённые в dataclass
        for field_name, field_info in self.__dataclass_fields__.items():  # type: ignore[attr-defined]
            value: Any = getattr(self, field_name)  # Получаем значение поля
            # Проверяем тип UUID
            if field_info.type == UUID:
                self._validate_uuid(value)
            # Преобразуем rating в float, если он существует и не является float
            if field_name == "rating" and value is not None and not isinstance(value, float):
                setattr(self, field_name, float(value))
            # Преобразуем created_at в datetime
            if field_name == "created_at" and value is not None and not isinstance(value, datetime):
                setattr(self, field_name, datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f+00'))
            # Преобразуем updated_at в datetime
            if field_name == "updated_at" and value is not None and not isinstance(value, datetime):
                setattr(self, field_name, datetime.strptime(value, '%Y-%m-%d %H:%M:%S.%f+00'))