import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mamacare_secret_key_2026_maternal_portal_final_year')
    DB_TYPE = os.environ.get('DB_TYPE', 'mysql') # 'mysql' or 'sqlite'
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'mamacare_db')
    
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLITE_PATH = os.path.join(BASE_DIR, 'database', 'mamacare.db')