from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def crear_base_datos():
    conn = sqlite3.connect("instituto.db")

    conn.execute("""
    CREATE TABLE IF NOT EXISTS carreras (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        duracion INTEGER NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS estudiantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellidos TEXT NOT NULL,
        fecha_nacimiento DATE NOT NULL
    )
    """)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS matriculas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fecha DATE NOT NULL,
        carrera_id INTEGER NOT NULL,
        estudiante_id INTEGER NOT NULL,
        FOREIGN KEY (carrera_id) REFERENCES carreras(id),
        FOREIGN KEY (estudiante_id) REFERENCES estudiantes(id)
    )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def inicio():
    return render_template("index.html")


if __name__ == "__main__":
    crear_base_datos()
    app.run(debug=True)