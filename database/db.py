# database/db.py
import os
import sqlite3
import pymysql
from pymysql.cursors import DictCursor
from config import Config
from werkzeug.security import generate_password_hash

class DatabaseManager:
    def __init__(self):
        self.config = Config
        self.engine_type = None
        self._test_and_init()

    def _test_and_init(self):
        try:
            conn = pymysql.connect(
                host=self.config.MYSQL_HOST,
                port=self.config.MYSQL_PORT,
                user=self.config.MYSQL_USER,
                password=self.config.MYSQL_PASSWORD,
                charset='utf8mb4',
                cursorclass=DictCursor,
                connect_timeout=2
            )
            with conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE IF NOT EXISTS `{self.config.MYSQL_DB}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            conn.select_db(self.config.MYSQL_DB)
            conn.close()
            self.engine_type = 'mysql'
            print(f"[MamaCare DB] Connected to MySQL database '{self.config.MYSQL_DB}'.")
        except Exception as e:
            print(f"[MamaCare DB] MySQL not available ({e}). Using local SQLite fallback database.")
            self.engine_type = 'sqlite'
            os.makedirs(os.path.dirname(self.config.SQLITE_PATH), exist_ok=True)
            
        self.init_schema()

    def get_connection(self):
        if self.engine_type == 'mysql':
            return pymysql.connect(
                host=self.config.MYSQL_HOST,
                port=self.config.MYSQL_PORT,
                user=self.config.MYSQL_USER,
                password=self.config.MYSQL_PASSWORD,
                database=self.config.MYSQL_DB,
                charset='utf8mb4',
                cursorclass=DictCursor,
                autocommit=True
            )
        else:
            conn = sqlite3.connect(self.config.SQLITE_PATH)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON;")
            return conn

    def init_schema(self):
        if self.engine_type == 'mysql':
            conn = self.get_connection()
            with conn.cursor() as cur:
                cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(120) NOT NULL UNIQUE,
                    password_hash VARCHAR(255) NOT NULL,
                    lmp_date DATE NULL,
                    due_date DATE NULL,
                    blood_group VARCHAR(10) NULL,
                    emergency_contact_name VARCHAR(100) NULL,
                    emergency_contact_phone VARCHAR(20) NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                );
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS appointments (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    doctor_name VARCHAR(100) NOT NULL,
                    clinic_hospital VARCHAR(150) NOT NULL,
                    appointment_date DATE NOT NULL,
                    appointment_time TIME NOT NULL,
                    reason VARCHAR(200) NOT NULL,
                    notes TEXT NULL,
                    is_completed BOOLEAN DEFAULT FALSE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS medicine_reminders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    medicine_name VARCHAR(100) NOT NULL,
                    dosage VARCHAR(50) NOT NULL,
                    frequency VARCHAR(50) NOT NULL,
                    reminder_time TIME NOT NULL,
                    instructions VARCHAR(100) DEFAULT 'With food',
                    is_active BOOLEAN DEFAULT TRUE,
                    last_taken_date DATE NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS contact_messages (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    email VARCHAR(120) NOT NULL,
                    phone VARCHAR(20) NULL,
                    subject VARCHAR(150) NOT NULL,
                    message TEXT NOT NULL,
                    status VARCHAR(20) DEFAULT 'Unread',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS meal_reminders (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    meal_name VARCHAR(150) NOT NULL,
                    meal_type VARCHAR(50) NOT NULL,
                    reminder_time TIME NOT NULL,
                    notes TEXT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                """)
                cur.execute("""
                CREATE TABLE IF NOT EXISTS user_diet_preferences (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL UNIQUE,
                    trimester INT DEFAULT 2,
                    pregnancy_week INT DEFAULT 20,
                    dietary_preference VARCHAR(100) DEFAULT 'Vegetarian',
                    allergies TEXT NULL,
                    dietary_restrictions TEXT NULL,
                    foods_usually_eaten TEXT NULL,
                    medical_conditions TEXT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
                );
                """)
            conn.close()
        else:
            conn = self.get_connection()
            cur = conn.cursor()
            cur.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                lmp_date TEXT NULL,
                due_date TEXT NULL,
                blood_group TEXT NULL,
                emergency_contact_name TEXT NULL,
                emergency_contact_phone TEXT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                doctor_name TEXT NOT NULL,
                clinic_hospital TEXT NOT NULL,
                appointment_date TEXT NOT NULL,
                appointment_time TEXT NOT NULL,
                reason TEXT NOT NULL,
                notes TEXT NULL,
                is_completed INTEGER DEFAULT 0,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS medicine_reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                medicine_name TEXT NOT NULL,
                dosage TEXT NOT NULL,
                frequency TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                instructions TEXT DEFAULT 'With food',
                is_active INTEGER DEFAULT 1,
                last_taken_date TEXT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS contact_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NULL,
                subject TEXT NOT NULL,
                message TEXT NOT NULL,
                status TEXT DEFAULT 'Unread',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS meal_reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                meal_name TEXT NOT NULL,
                meal_type TEXT NOT NULL,
                reminder_time TEXT NOT NULL,
                notes TEXT NULL,
                is_active INTEGER DEFAULT 1,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS user_diet_preferences (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL UNIQUE,
                trimester INTEGER DEFAULT 2,
                pregnancy_week INTEGER DEFAULT 20,
                dietary_preference TEXT DEFAULT 'Vegetarian',
                allergies TEXT NULL,
                dietary_restrictions TEXT NULL,
                foods_usually_eaten TEXT NULL,
                medical_conditions TEXT NULL,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            );
            """)
            conn.commit()
            
            user_check = cur.execute("SELECT COUNT(*) FROM users").fetchone()[0]
            if user_check == 0:
                demo_hash = generate_password_hash('password123')
                cur.execute("""
                INSERT INTO users (name, email, password_hash, lmp_date, due_date, blood_group, emergency_contact_name, emergency_contact_phone)
                VALUES (?, ?, ?, date('now', '-140 days'), date('now', '+140 days'), 'O+', 'Michael Johnson (Husband)', '+1 (555) 234-5678')
                """, ('Sarah Johnson', 'sarah@example.com', demo_hash))
                user_id = cur.lastrowid
                
                cur.execute("""
                INSERT INTO appointments (user_id, doctor_name, clinic_hospital, appointment_date, appointment_time, reason, notes, is_completed)
                VALUES (?, ?, ?, date('now', '+5 days'), '10:30', '20-Week Anatomy Ultrasound Scan', 'Drink 2 glasses of water prior to appointment.', 0)
                """, (user_id, 'Dr. Emily Carter, OB-GYN', 'City Maternity Hospital, Suite 302'))

                cur.execute("""
                INSERT INTO appointments (user_id, doctor_name, clinic_hospital, appointment_date, appointment_time, reason, notes, is_completed)
                VALUES (?, ?, ?, date('now', '+20 days'), '14:00', 'Routine Prenatal Checkup & Blood Pressure', 'Discuss iron supplement dosage.', 0)
                """, (user_id, 'Dr. Robert Davis', 'Wellness Family Clinic'))

                cur.execute("""
                INSERT INTO medicine_reminders (user_id, medicine_name, dosage, frequency, reminder_time, instructions, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, 'Prenatal Multivitamin with DHA', '1 Tablet', 'Once daily', '08:30', 'After breakfast', 1))

                cur.execute("""
                INSERT INTO medicine_reminders (user_id, medicine_name, dosage, frequency, reminder_time, instructions, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, 'Ferrous Sulfate (Iron)', '65 mg', 'Once daily', '13:00', 'Take with orange juice (Vit C)', 1))

                cur.execute("""
                INSERT INTO medicine_reminders (user_id, medicine_name, dosage, frequency, reminder_time, instructions, is_active)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (user_id, 'Calcium + Vit D3', '500 mg', 'Twice daily', '20:00', 'With dinner or at bedtime', 1))

                # Seed Meal Reminders
                cur.execute("""
                INSERT INTO meal_reminders (user_id, meal_name, meal_type, reminder_time, notes, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, 'Warm Oatmeal with Walnuts & Chia Seeds', 'Breakfast', '08:00', 'Rich in iron, folate and slow-release carbs', 1))

                cur.execute("""
                INSERT INTO meal_reminders (user_id, meal_name, meal_type, reminder_time, notes, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, 'Greek Yogurt with Sliced Strawberries', 'Morning Snack', '11:00', 'High calcium and protein boost', 1))

                cur.execute("""
                INSERT INTO meal_reminders (user_id, meal_name, meal_type, reminder_time, notes, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, 'Spinach Lentil Bowl with Brown Rice & Avocado', 'Lunch', '13:00', 'Plant iron paired with healthy fats for DHA absorption', 1))

                cur.execute("""
                INSERT INTO meal_reminders (user_id, meal_name, meal_type, reminder_time, notes, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, 'Roasted Chickpeas & 1 Glass Lemon Water', 'Evening Snack', '17:00', 'High fiber and hydration replenisher', 1))

                cur.execute("""
                INSERT INTO meal_reminders (user_id, meal_name, meal_type, reminder_time, notes, is_active)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (user_id, 'Steamed Vegetables with Paneer/Tofu & Quinoa', 'Dinner', '20:00', 'Light, easily digestible to avoid nighttime heartburn', 1))
                
                # Seed User Diet Preferences
                cur.execute("""
                INSERT INTO user_diet_preferences (user_id, trimester, pregnancy_week, dietary_preference, allergies, dietary_restrictions, foods_usually_eaten, medical_conditions)
                VALUES (?, 2, 20, 'Vegetarian', 'None', 'Low Sodium', 'Oatmeal, Lentil soup, Paneer, Spinach, Bananas, Apples, Yogurt, Brown Rice', 'None')
                """, (user_id,))

                conn.commit()
            conn.close()

    def query(self, sql, params=None, fetchone=False, fetchall=False, commit=False, return_lastrowid=False):
        params = params or ()
        conn = self.get_connection()
        try:
            if self.engine_type == 'mysql':
                formatted_sql = sql.replace('?', '%s')
                with conn.cursor() as cur:
                    cur.execute(formatted_sql, params)
                    if commit:
                        conn.commit()
                    if return_lastrowid:
                        return cur.lastrowid
                    if fetchone:
                        return cur.fetchone()
                    if fetchall:
                        return cur.fetchall()
            else:
                formatted_sql = sql.replace('%s', '?')
                cur = conn.cursor()
                cur.execute(formatted_sql, params)
                if commit:
                    conn.commit()
                if return_lastrowid:
                    res = cur.lastrowid
                    conn.close()
                    return res
                if fetchone:
                    row = cur.fetchone()
                    res = dict(row) if row else None
                    conn.close()
                    return res
                if fetchall:
                    rows = cur.fetchall()
                    res = [dict(r) for r in rows]
                    conn.close()
                    return res
        finally:
            if self.engine_type == 'mysql':
                conn.close()

db = DatabaseManager()