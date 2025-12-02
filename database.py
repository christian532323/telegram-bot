import sqlite3

# Conexión a la base de datos SQLite
conn = sqlite3.connect("db.sqlite3", check_same_thread=False)
cursor = conn.cursor()

# Tabla de usuarios
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT,
    credits INTEGER DEFAULT 0,
    is_admin INTEGER DEFAULT 0
)
""")

# Tabla de productos
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    description TEXT
)
""")

# Tabla de opciones (ejemplo: 1 día, 7 días, 30 días)
cursor.execute("""
CREATE TABLE IF NOT EXISTS product_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    option_name TEXT,
    price REAL,
    stock INTEGER,
    FOREIGN KEY(product_id) REFERENCES products(id)
)
""")

##############################
# FUNCIONES DE LA BASE DE DATOS
##############################

def add_user(user_id, username, is_admin=0):
    cursor.execute(
        "INSERT OR IGNORE INTO users (id, username, is_admin) VALUES (?, ?, ?)",
        (user_id, username, is_admin)
    )
    conn.commit()


def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    return cursor.fetchone()


def get_products():
    cursor.execute("SELECT * FROM products")
    return cursor.fetchall()


def get_product_options(product_id):
    cursor.execute("SELECT * FROM product_options WHERE product_id=?", (product_id,))
    return cursor.fetchall()
