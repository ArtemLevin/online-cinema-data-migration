import sqlite3
import psycopg
from psycopg import ClientCursor, connection as _connection
from psycopg.rows import dict_row
from postgres_saver import PostgresSaver
from sqlite_loader import SQLiteLoader
from test_transfer import TestTransfer

def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection, table_name: str):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn, table_name)
    sqlite_loader = SQLiteLoader(connection, table_name)

    data = sqlite_loader.load_movies()

    postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = {'dbname': 'movies_database', 'user': 'app', 'password': '123qwe', 'host': '127.0.0.1', 'port': 5432}
    with sqlite3.connect('sqlite.db') as sqlite_conn, psycopg.connect(
            **dsl, row_factory=dict_row, cursor_factory=ClientCursor
    ) as pg_conn:
        for table_name in ['film_work', 'genre', 'genre_film_work', 'person', 'person_film_work']:
            load_from_sqlite(sqlite_conn, pg_conn, table_name)
        for table_name in ['film_work', 'genre', 'genre_film_work', 'person', 'person_film_work']:
            TestTransfer(sqlite_conn, pg_conn, table_name).test_transfer()
            print(f'Table {table_name} was successfully transferred to PostgreSQL.')