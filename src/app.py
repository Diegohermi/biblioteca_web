from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# Conexión a SQLite
conn = sqlite3.connect("biblioteca.db", check_same_thread=False)
cursor = conn.cursor()

# Crear tablas si no existen
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS libros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    autor TEXT NOT NULL,
    editorial TEXT,
    anio INTEGER,
    disponible INTEGER DEFAULT 1
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS prestamos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    libro_id INTEGER NOT NULL,
    fecha_prestamo TEXT NOT NULL,
    fecha_devolucion TEXT,
    FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
    FOREIGN KEY(libro_id) REFERENCES libros(id)
)
""")

# Insertar datos iniciales si las tablas están vacías
cursor.execute("SELECT COUNT(*) FROM usuarios")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO usuarios (nombre, correo, password) VALUES (?, ?, ?)",
                   ("Diego", "diego@test.com", "1234"))

cursor.execute("SELECT COUNT(*) FROM libros")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO libros (titulo, autor, editorial, anio) VALUES (?, ?, ?, ?)",
                   ("Cien años de soledad", "Gabriel García Márquez", "Sudamericana", 1967))
    cursor.execute("INSERT INTO libros (titulo, autor, editorial, anio) VALUES (?, ?, ?, ?)",
                   ("El Principito", "Antoine de Saint-Exupéry", "Reynal & Hitchcock", 1943))

cursor.execute("SELECT COUNT(*) FROM prestamos")
if cursor.fetchone()[0] == 0:
    cursor.execute("INSERT INTO prestamos (usuario_id, libro_id, fecha_prestamo, fecha_devolucion) VALUES (?, ?, ?, ?)",
                   (1, 1, "2024-01-15", None))

conn.commit()

# Rutas principales
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/usuarios")
def listar_usuarios():
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    return render_template("usuarios.html", usuarios=usuarios)

@app.route("/libros")
def listar_libros():
    cursor.execute("SELECT * FROM libros")
    libros = cursor.fetchall()
    return render_template("libros.html", libros=libros)

@app.route("/prestamos")
def listar_prestamos():
    cursor.execute("SELECT * FROM prestamos")
    prestamos = cursor.fetchall()
    return render_template("prestamos.html", prestamos=prestamos)

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Puerto cambiado a 5001
