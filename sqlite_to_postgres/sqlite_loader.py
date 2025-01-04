import sqlite3
from typing import Generator
import logging
from film_work_dataclass import FilmWork
from genre_dataclass import Genre
from genre_film_work_dataclass import GenreFilmWork
from person_dataclass import Person
from person_film_work_dataclass import PersonFilmWork

logger = logging.getLogger(__name__)


class SQLiteLoader:
    """
    Класс для извлечения данных из SQLite базы данных и их обработки партиями (batch).
    """

    TABLE_TO_DATACLASS = {
        'film_work': FilmWork,
        'genre': Genre,
        'person': Person,
        'person_film_work': PersonFilmWork,
        'genre_film_work': GenreFilmWork,
    }

    def __init__(self, connection, table_name, batch=100):
        """
        Инициализирует объект SQLiteLoader.

        :param connection: Объект подключения к SQLite базе данных (sqlite3.Connection).
        :param table_name: Имя таблицы, из которой будут извлекаться данные.
        :param batch: Размер партии данных, которые будут извлекаться из базы (по умолчанию 100).
        :raises ValueError: Если переданы некорректные параметры.
        """
        self._validate_connection(connection)
        self._validate_batch_size(batch)
        self._validate_table_name(table_name)

        self.connection = connection
        self.table_name = table_name
        self.batch = batch

    def _validate_connection(self, connection):
        """Проверяет, что переданный объект подключения является валидным."""
        if not hasattr(connection, 'cursor'):
            raise ValueError("Provided connection object is not a valid SQLite connection.")

    def _validate_batch_size(self, batch):
        """Проверяет, что размер партии является положительным целым числом."""
        if not isinstance(batch, int) or batch <= 0:
            raise ValueError("Batch size must be a positive integer.")

    def _validate_table_name(self, table_name):
        """Проверяет, что имя таблицы поддерживается."""
        if not isinstance(table_name, str):
            raise ValueError("table_name must be a string.")
        if table_name not in self.TABLE_TO_DATACLASS:
            raise ValueError(f"Invalid table name: {table_name}")

    def extract_data(self, sqlite_cursor: sqlite3.Cursor) -> Generator[list[sqlite3.Row], None, None]:
        """
        Извлекает данные из таблицы партиями.

        :param sqlite_cursor: Курсор SQLite для выполнения запросов к базе данных.
        :return: Генератор, который возвращает списки строк (batch) из таблицы.
        :raises RuntimeError: Если возникает ошибка при выполнении запроса или чтении данных.
        """
        try:
            # Выполняем SQL-запрос для получения всех данных из таблицы
            sqlite_cursor.execute(f'SELECT * FROM {self.table_name};')
        except sqlite3.OperationalError as e:
            # Логируем ошибку и выбрасываем исключение, если запрос не может быть выполнен
            logger.error(f"Failed to execute query: {e}")
            raise RuntimeError(f"Failed to execute query: {e}")

        # Бесконечный цикл для извлечения данных партиями
        while True:
            try:
                # Извлекаем партию строк из результата запроса
                results = sqlite_cursor.fetchmany(self.batch)
                if not results:  # Если партия пустая, прекращаем генерацию данных
                    break
                yield results  # Возвращаем текущую партию строк
            except sqlite3.InterfaceError as e:
                # Логируем ошибку, если возникает проблема с курсором или чтением данных
                logger.error(f"Error fetching data: {e}")
                raise RuntimeError(f"Error fetching data: {e}")

    def load_movies(self) -> Generator[list, None, None]:
        """
        Загружает данные из таблицы и преобразует их в объекты соответствующих датаклассам.

        :return: Генератор, который возвращает списки объектов текущего датакласса.
        :raises RuntimeError: Если возникает ошибка при создании курсора или преобразовании данных.
        """
        try:
            # Создаем курсор для выполнения запросов к базе данных
            sqlite_cursor = self.connection.cursor()
        except sqlite3.ProgrammingError as e:
            # Логируем ошибку и выбрасываем исключение, если не удалось создать курсор
            logger.error(f"Failed to create cursor: {e}")
            raise RuntimeError(f"Failed to create cursor: {e}")

        dataclass = self.TABLE_TO_DATACLASS[self.table_name]

        # Извлекаем данные партиями с помощью метода extract_data
        for batch in self.extract_data(sqlite_cursor):
            try:
                yield [dataclass(*row) for row in batch]
            except (TypeError, ValueError) as e:
                logger.error(f"Failed to create objects for table {self.table_name}: {e}")
                raise RuntimeError(f"Failed to create objects for table {self.table_name}: {e}")