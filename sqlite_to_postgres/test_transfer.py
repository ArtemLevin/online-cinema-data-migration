import sqlite3
import psycopg
from uuid import UUID
from film_work_dataclass import FilmWork
from genre_dataclass import Genre
from genre_film_work_dataclass import GenreFilmWork
from person_dataclass import Person
from person_film_work_dataclass import PersonFilmWork





import logging

class TestTransfer():

    TABLE_TO_DATACLASS = {
        'film_work': FilmWork,
        'genre': Genre,
        'person': Person,
        'person_film_work': PersonFilmWork,
        'genre_film_work': GenreFilmWork,
    }


    def __init__(self, sqlite_conn: sqlite3.Connection, pg_conn: psycopg.Connection, table_name: str, batch: int = 100) -> None:
        self.sqlite_conn = sqlite_conn
        self.pg_conn = pg_conn
        self.batch = batch
        self.table_name = table_name
        self.dataclass = self.TABLE_TO_DATACLASS[table_name]
        self.logger = logging.getLogger(__name__)

    def test_transfer(self) -> None:
        try:
            # Открываем курсоры для SQLite и PostgreSQL
            sqlite_cursor = self.sqlite_conn.cursor()
            pg_cursor = self.pg_conn.cursor()

            # Выполняем запрос к SQLite
            sqlite_cursor.execute('SELECT * FROM {table}'.format(table=self.table_name))

            while batch := sqlite_cursor.fetchmany(self.batch):
                try:
                    # Преобразуем результаты запроса SQLite в объекты dataclass
                    original_data_batch = [self.dataclass(*row) for row in batch]
                    ids = [data.id for data in original_data_batch]
                    # Выполняем запрос к PostgreSQL для получения данных
                    pg_cursor.execute('SELECT * FROM content.{table} WHERE id = ANY(%s)'.format(table=self.table_name), [ids])

                    transferred_data_batch = [self.dataclass(**row) for row in pg_cursor.fetchall()]
                    for data in original_data_batch:
                        for item in transferred_data_batch:
                            if data.id == item.id:
                                assert data == item, (f"{data} \nnot equal to {item}")

                    # Проверяем количество
                    assert len(original_data_batch) == len(transferred_data_batch), \
                        "Batch size mismatch between SQLite and PostgreSQL."


                except AssertionError as e:
                    # Логируем ошибку, если данные не совпадают
                    self.logger.error(f"Data mismatch: {e}")
                    raise RuntimeError(f"Data mismatch: {e}")

        except sqlite3.Error as e:
            self.logger.error(f"SQLite operation failed: {e}")
            raise RuntimeError(f"SQLite operation failed: {e}")

        except psycopg.Error as e:
            self.logger.error(f"PostgreSQL operation failed: {e}")
            raise RuntimeError(f"PostgreSQL operation failed: {e}")

        except Exception as e:
            self.logger.error(f"Unexpected error occurred: {e}")
            raise RuntimeError(f"Unexpected error occurred: {e}")

        finally:
            # Закрываем курсоры
            sqlite_cursor.close()
            pg_cursor.close()



