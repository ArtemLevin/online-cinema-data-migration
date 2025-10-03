# 🎬 Admin Panel & Data Migration Project

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-green?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-blue?logo=postgresql&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-lightgrey?logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-yellow)

**Database schema design**, **Django admin customization**, and **data migration** from SQLite to PostgreSQL for online cinema project.

---

## 📦 Project Structure

- **`schema_design/`** – DDL scripts for creating the PostgreSQL database schema (`content` schema).  
- **`movies_admin/`** – Django application with:  
  - models for films, genres, and persons;  
  - a customizable admin panel;  
  - localization support (RU/EN);  
  - PostgreSQL configuration via `.env`.  
- **`sqlite_to_postgres/`** – Data migration scripts with:  
  - batch data loading from SQLite;  
  - PostgreSQL inserts with error handling;  
  - migration validation tests.  

---

## ⚙️ Installation & Setup

### 1. Clone the repository
```bash
git clone https://github.com/ArtemLevin/online-cinema-data-migration.git
cd new_admin_panel
```

### 2. Create virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate    # Windows

pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the project root:

```env
DB_NAME=movies_database
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=127.0.0.1
DB_PORT=5432
SECRET_KEY=django-secret-key
SQLITE_DB=db.sqlite3
```

### 4. Apply migrations & run Django
```bash
cd movies_admin
python manage.py migrate
python manage.py runserver
```

### 5. Run data migration
```bash
cd sqlite_to_postgres
python load_data.py
```

---

## 🚀 Features

- Database design with **UUID keys, indexes, and constraints**.  
- Django admin with **filters, search, and many-to-many relations**.  
- Full **localization support** (Russian & English).  
- Migration scripts with **data validation and error handling**.  
- Automated tests to validate migration correctness (`TestTransfer`).  

---

## 📚 Requirements

- Python 3.10+  
- Django 4.2+  
- PostgreSQL 13+  
- SQLite 3  
- psycopg 3  

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!  
Feel free to open an [issue](../../issues) or submit a [pull request](../../pulls).

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
