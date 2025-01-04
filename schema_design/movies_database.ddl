
-- Создание схемы
CREATE SCHEMA IF NOT EXISTS content;

-- Таблица фильмов
CREATE TABLE IF NOT EXISTS content.film_work (
    id UUID PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    creation_date DATE,
    file_path TEXT,
    rating DECIMAL(2,1) CHECK (rating >= 0 AND rating <= 10),
    type VARCHAR NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица жанров
CREATE TABLE IF NOT EXISTS content.genre (
    id UUID PRIMARY KEY,
    name VARCHAR(50),
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица персон
CREATE TABLE IF NOT EXISTS content.person (
    id UUID PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Связь жанров и фильмов
CREATE TABLE IF NOT EXISTS content.genre_film_work (
    id UUID PRIMARY KEY,
    film_work_id UUID NOT NULL,
    genre_id UUID NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (genre_id) REFERENCES content.genre (id) ON DELETE CASCADE,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    UNIQUE (genre_id, film_work_id)
);

-- Связь персон и фильмов
CREATE TABLE IF NOT EXISTS content.person_film_work (
    id UUID PRIMARY KEY,
    film_work_id UUID NOT NULL,
    person_id UUID NOT NULL,
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (person_id) REFERENCES content.person (id) ON DELETE CASCADE,
    FOREIGN KEY (film_work_id) REFERENCES content.film_work (id) ON DELETE CASCADE,
    UNIQUE (person_id, film_work_id, role)
);

-- Индексы для ускорения запросов
CREATE INDEX if not exists idx_genre_film_work_genre_id_film_work_id ON content.genre_film_work (genre_id, film_work_id);
CREATE INDEX if not exists idx_person_film_work_person_id_film_work_id ON content.person_film_work (person_id, film_work_id);
CREATE INDEX if not exists idx_person_film_work_role ON content.person_film_work (role);
