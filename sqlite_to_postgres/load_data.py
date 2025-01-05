import sqlite3
import psycopg
import os
import logging
from psycopg import ClientCursor, connection as _connection
from contextlib import contextmanager
from psycopg.rows import dict_row
from postgres_saver import PostgresSaver
from sqlite_loader import SQLiteLoader
from test_transfer import TestTransfer
from dotenv import load_dotenv

load_dotenv()

# Логирование
logging.basicConfig(level=logging.INFO)

# Контекстный менеджер для SQLite
@contextmanager
def open_db(file_name: str):
    conn = sqlite3.connect(file_name)
    try:
        logging.info("Creating SQLite connection")
        yield conn.cursor()  # Возвращаем курсор
    finally:
        logging.info("Closing SQLite connection")
        conn.commit()
        conn.close()

def load_from_sqlite(cursor: ClientCursor, pg_conn: _connection, table_name: str):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn, table_name)
    sqlite_loader = SQLiteLoader(cursor, table_name)

    data = sqlite_loader.load_movies()

    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {
        'dbname': os.getenv('DB_NAME'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT')

    }
    # Использование контекстного менеджера для SQLite и PostgreSQL
    with open_db(file_name=os.getenv('SQLITE_DB')) as sqlite_cursor, psycopg.connect(
            **dsl, row_factory=dict_row, cursor_factory=ClientCursor
    ) as pg_conn:
        # Перенос данных из SQLite в PostgreSQL
        for table_name in ['film_work', 'genre', 'genre_film_work', 'person', 'person_film_work']:
            load_from_sqlite(sqlite_cursor, pg_conn, table_name)

        # Тестирование переноса данных
        for table_name in ['film_work', 'genre', 'genre_film_work', 'person', 'person_film_work']:
            TestTransfer(sqlite_cursor, pg_conn, table_name).test_transfer()
            logging.info(f'Table {table_name} was successfully transferred to PostgreSQL.')
