from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)


# ==========================================
# CREAR BASE DE DATOS
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
# INICIO
# ==========================================

@app.route("/")
def inicio():
    return render_template("index.html")


# ==========================================
# CARRERAS - LISTAR
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
# CARRERAS - REGISTRAR
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
# CARRERAS - EDITAR
# ==========================================

@app.route("/carreras/editar/<int:id>", methods=["GET", "POST"])
def editar_carrera(id):

    conn = sqlite3.connect("instituto.db")
    conn.row_factory = sqlite3.Row

    carrera = conn.execute(
        "SELECT * FROM carreras WHERE id = ?",
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
# CARRERAS - ELIMINAR
# ==========================================

@app.route("/carreras/eliminar/<int:id>")
def eliminar_carrera(id):

    conn = sqlite3.connect("instituto.db")

    conn.execute(
        "DELETE FROM carreras WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/carreras")


# ==========================================
# ESTUDIANTES - LISTAR
# ==========================================

@app.route("/estudiantes")
def estudiantes():

    conn = sqlite3.connect("instituto.db")
    conn.row_factory = sqlite3.Row

    datos = conn.execute(
        "SELECT * FROM estudiantes"
    ).fetchall()

    conn.close()

    return render_template(
        "estudiantes.html",
        estudiantes=datos
    )


# ==========================================
# ESTUDIANTES - REGISTRAR
# ==========================================

@app.route("/estudiantes/nuevo", methods=["GET", "POST"])
def nuevo_estudiante():

    if request.method == "POST":

        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        fecha_nacimiento = request.form["fecha_nacimiento"]

        conn = sqlite3.connect("instituto.db")

        conn.execute(
            """
            INSERT INTO estudiantes
            (nombre, apellidos, fecha_nacimiento)
            VALUES (?, ?, ?)
            """,
            (nombre, apellidos, fecha_nacimiento)
        )

        conn.commit()
        conn.close()

        return redirect("/estudiantes")

    return render_template("nuevo_estudiante.html")


# ==========================================
# ESTUDIANTES - EDITAR
# ==========================================

@app.route("/estudiantes/editar/<int:id>", methods=["GET", "POST"])
def editar_estudiante(id):

    conn = sqlite3.connect("instituto.db")
    conn.row_factory = sqlite3.Row

    estudiante = conn.execute(
        "SELECT * FROM estudiantes WHERE id = ?",
        (id,)
    ).fetchone()

    if request.method == "POST":

        nombre = request.form["nombre"]
        apellidos = request.form["apellidos"]
        fecha_nacimiento = request.form["fecha_nacimiento"]

        conn.execute(
            """
            UPDATE estudiantes
            SET nombre = ?,
                apellidos = ?,
                fecha_nacimiento = ?
            WHERE id = ?
            """,
            (nombre, apellidos, fecha_nacimiento, id)
        )

        conn.commit()
        conn.close()

        return redirect("/estudiantes")

    conn.close()

    return render_template(
        "editar_estudiante.html",
        estudiante=estudiante
    )


# ==========================================
# ESTUDIANTES - ELIMINAR
# ==========================================

@app.route("/estudiantes/eliminar/<int:id>")
def eliminar_estudiante(id):

    conn = sqlite3.connect("instituto.db")

    conn.execute(
        "DELETE FROM estudiantes WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/estudiantes")


# ==========================================
# MATRÍCULAS - LISTAR
# ==========================================

@app.route("/matriculas")
def matriculas():

    conn = sqlite3.connect("instituto.db")
    conn.row_factory = sqlite3.Row

    datos = conn.execute("""
        SELECT
            matriculas.id,
            matriculas.fecha,
            estudiantes.nombre || ' ' || estudiantes.apellidos AS estudiante,
            carreras.nombre AS carrera
        FROM matriculas
        INNER JOIN estudiantes
            ON matriculas.estudiante_id = estudiantes.id
        INNER JOIN carreras
            ON matriculas.carrera_id = carreras.id
        ORDER BY matriculas.id
    """).fetchall()

    conn.close()

    return render_template(
        "matriculas.html",
        matriculas=datos
    )


# ==========================================
# MATRÍCULAS - REGISTRAR
# ==========================================

@app.route("/matriculas/nueva", methods=["GET", "POST"])
def nueva_matricula():

    conn = sqlite3.connect("instituto.db")
    conn.row_factory = sqlite3.Row

    if request.method == "POST":

        fecha = request.form["fecha"]
        carrera_id = request.form["carrera_id"]
        estudiante_id = request.form["estudiante_id"]

        conn.execute(
            """
            INSERT INTO matriculas
            (fecha, carrera_id, estudiante_id)
            VALUES (?, ?, ?)
            """,
            (fecha, carrera_id, estudiante_id)
        )

        conn.commit()
        conn.close()

        return redirect("/matriculas")

    carreras = conn.execute(
        "SELECT * FROM carreras"
    ).fetchall()

    estudiantes = conn.execute(
        "SELECT * FROM estudiantes"
    ).fetchall()

    conn.close()

    return render_template(
        "nueva_matricula.html",
        carreras=carreras,
        estudiantes=estudiantes
    )


# ==========================================
# MATRÍCULAS - ELIMINAR
# ==========================================

@app.route("/matriculas/eliminar/<int:id>")
def eliminar_matricula(id):

    conn = sqlite3.connect("instituto.db")

    conn.execute(
        "DELETE FROM matriculas WHERE id = ?",
        (id,)
    )

    conn.commit()
    conn.close()

    return redirect("/matriculas")


# ==========================================
# EJECUTAR APLICACIÓN
# ==========================================

if __name__ == "__main__":

    crear_base_datos()

    app.run(debug=True)