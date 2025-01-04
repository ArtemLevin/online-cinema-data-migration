from dataclasses import astuple, dataclass
import psycopg
from psycopg.errors import DatabaseError
import logging
from film_work_dataclass import FilmWork
from genre_dataclass import Genre
from genre_film_work_dataclass import GenreFilmWork
from person_dataclass import Person
from person_film_work_dataclass import PersonFilmWork

logger = logging.getLogger(__name__)


class PostgresSaver:
    """
    Класс для сохранения данных в таблицу PostgreSQL.
    """
    TABLE_TO_DATACLASS = {
        'film_work':
            {
                'dataclass': FilmWork,
                'fields': ['id', 'title', 'description', 'creation_date', 'file_path', 'rating', 'type', 'created_at',
                           'updated_at'],
            },
        'genre':
            {
                'dataclass': Genre,
                'fields': ['id', 'name', 'description', 'created_at', 'updated_at'],

            },
        'person':
            {
                'dataclass': Person,
                'fields': ['id', 'full_name', 'created_at', 'updated_at', ]

            },
        'person_film_work':
            {
                'dataclass': PersonFilmWork,
                'fields': ['id', 'film_work_id', 'person_id', 'role', 'created_at']

            },
        'genre_film_work':
            {
                'dataclass': GenreFilmWork,
                'fields': ['id', 'film_work_id', 'genre_id', 'created_at', ]
            },

    }

    def __init__(self, connection: psycopg.Connection, table_name: str, batch: int = 100):
        """
        Инициализирует объект PostgresSaver.

        :param connection: Объект подключения к PostgreSQL.
        :param table_name: Имя таблицы для сохранения данных.
        :param batch: Размер партии данных для вставки (по умолчанию 100).
        """
        self._validate_connection(connection)
        self._validate_table_name(table_name)

        self.connection = connection
        self.table_name = table_name
        self.batch = batch

        self.dataclass = self.TABLE_TO_DATACLASS[table_name]['dataclass']
        self.fields = self.TABLE_TO_DATACLASS[table_name]['fields']
        self.insert_query = self._build_insert_query()

    def _build_insert_query(self) -> str:
        placeholders = ', '.join(['%s'] * len(self.fields))
        query = f"""
            INSERT INTO content.{self.table_name} ({', '.join(self.fields)})
            VALUES ({placeholders})
            ON CONFLICT DO NOTHING;
        """
        return query

    def _validate_connection(self, connection: psycopg.Connection) -> None:
        """Проверяет валидность подключения."""
        if not hasattr(connection, 'cursor'):
            raise ValueError("Provided connection object is not a valid PostgreSQL connection.")

    def _validate_table_name(self, table_name: str) -> None:
        """Проверяет, что имя таблицы поддерживается."""
        if table_name not in self.TABLE_TO_DATACLASS:
            raise ValueError(f"Invalid table name: {table_name}")

    def save_all_data(self, data: list[list[dataclass]]) -> None:
        """
        Сохраняет данные в таблицу PostgreSQL партиями.

        :param pg_cursor: Курсор PostgreSQL для выполнения запросов.
        :param data: Список партий данных, каждая из которых представляет собой список объектов dataclass.
        """
        total_inserted = 0
        for batch in data:
            try:
                # Проверяем, что все элементы в партии соответствуют dataclass
                if not all(isinstance(item, self.dataclass) for item in batch):
                    raise ValueError(
                        f"Batch contains invalid elements. All elements must be instances of {self.dataclass}.")

                # Преобразуем объекты dataclass в кортежи
                records = [astuple(item) for item in batch]

                # Вставляем данные с помощью executemany

                self.connection.cursor().executemany(self.insert_query, records)
                total_inserted += len(records)

                logger.info(f"Inserted batch of {len(records)} records into table '{self.table_name}'.")

            except (DatabaseError, ValueError) as e:
                logger.error(f"Failed to insert batch into PostgreSQL: {e}")
                self.connection.rollback()
                raise

        logger.info(f"Total records inserted into '{self.table_name}': {total_inserted}")
