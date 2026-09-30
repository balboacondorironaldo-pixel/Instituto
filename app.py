from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# ==========================================
# CREAR BASE DE DATOS Y TABLAS
# ==========================================

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


# ==========================================
# PÁGINA PRINCIPAL
# ==========================================

@app.route("/")
def inicio():

    return render_template("index.html")


# ==========================================
# MOSTRAR CARRERAS
# ==========================================

@app.route("/carreras")
def carreras():

    conn = sqlite3.connect("instituto.db")

    conn.row_factory = sqlite3.Row

    datos = conn.execute(
        "SELECT * FROM carreras"
    ).fetchall()

    conn.close()

    return render_template(
        "carreras.html",
        carreras=datos
    )


# ==========================================
# REGISTRAR NUEVA CARRERA
# ==========================================

@app.route("/carreras/nueva", methods=["GET", "POST"])
def nueva_carrera():

    if request.method == "POST":

        nombre = request.form["nombre"]

        duracion = request.form["duracion"]

        conn = sqlite3.connect("instituto.db")

        conn.execute(
            """
            INSERT INTO carreras (nombre, duracion)
            VALUES (?, ?)
            """,
            (nombre, duracion)
        )

        conn.commit()

        conn.close()

        return redirect("/carreras")

    return render_template("nueva_carrera.html")


# ==========================================
# EDITAR CARRERA
# ==========================================

@app.route("/carreras/editar/<int:id>", methods=["GET", "POST"])
def editar_carrera(id):

    conn = sqlite3.connect("instituto.db")

    conn.row_factory = sqlite3.Row

    carrera = conn.execute(
        """
        SELECT * FROM carreras
        WHERE id = ?
        """,
        (id,)
    ).fetchone()

    if request.method == "POST":

        nombre = request.form["nombre"]

        duracion = request.form["duracion"]

        conn.execute(
            """
            UPDATE carreras
            SET nombre = ?, duracion = ?
            WHERE id = ?
            """,
            (nombre, duracion, id)
        )

        conn.commit()

        conn.close()

        return redirect("/carreras")

    conn.close()

    return render_template(
        "editar_carrera.html",
        carrera=carrera
    )


# ==========================================
# ELIMINAR CARRERA
# ==========================================

@app.route("/carreras/eliminar/<int:id>")
def eliminar_carrera(id):

    conn = sqlite3.connect("instituto.db")

    conn.execute(
        """
        DELETE FROM carreras
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()

    conn.close()

    return redirect("/carreras")


# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================

if __name__ == "__main__":

    crear_base_datos()

    app.run(debug=True)