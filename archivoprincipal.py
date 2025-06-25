from flask import Flask, request, jsonify
import sqlite3
import requests
import os

app = Flask(__name__)

class Boliche:
    def __init__(self, nombre, dias, musica, edad_minima, perfil):
        self.nombre = nombre
        self.dias = dias
        self.musica = musica
        self.edad_minima = edad_minima
        self.perfil = perfil

    def to_dict(self):
        return self.__dict__

def crear_base_si_no_existe():
    conn = sqlite3.connect("base_datos.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS boliches (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        dias TEXT,
        musica TEXT,
        edad_minima INTEGER,
        perfil TEXT
    )
    """)
    cursor.execute("SELECT COUNT(*) FROM boliches")
    if cursor.fetchone()[0] == 0:
        boliches = [
            ("INK Buenos Aires", "Jueves, Viernes, Sábados", "Pop, Reggaetón, House", 18, "Fiestero"),
            ("Kika Club", "Jueves, Viernes, Sábados", "Electrónica, 80s, Pop, Hip Hop", 18, "Under"),
            ("Vita Live Buenos Aires", "Sábados", "Cachengue, Reggaetón, Pop", 18, "Exclusivo"),
            ("Sky Mood by Porto", "Sábados", "Cachengue", 18, "Fiestero"),
            ("Club Severino", "Lunes", "Hip Hop, Trap, House, Reggaetón, EDM", 18, "Mixto"),
            ("Pacha Buenos Aires", "Jueves, Viernes, Sábados", "Electrónica", 18, "Clásico"),
            ("Jet Lounge", "Jueves, Viernes, Sábados", "Electrónica, House, Hip Hop", 18, "Trendy"),
            ("Mandarine Park", "Sábados", "Electrónica, Pop, Reggaetón", 18, "Fashion"),
            ("Tequila Club", "Viernes, Sábados", "Reggaetón, Pop, Hip Hop", 21, "Exclusivo"),
            ("Terrazas del Este", "Miércoles, Sábados", "Electrónica, Reggaetón, Pop", 18, "Aire libre"),
            ("El Muelle Costanera", "Sábados", "Electrónica, Techno", 18, "Moderno"),
            ("Caix", "Viernes, Sábados", "Electrónica, House, Hip Hop", 18, "Clásico"),
            ("Moscu Buenos Aires", "Viernes, Sábados", "Electrónica, Techno", 18, "Trendy"),
            ("Bali", "Viernes, Sábados", "Cachengue, Reggaetón, Pop", 18, "Fiestero"),
            ("Museum", "Viernes, Sábados", "Reggaetón, RKT, Electrónica", 21, "Histórico"),
            ("Mata", "Viernes, Sábados", "Electrónica, House", 18, "Moderno"),
            ("Tamarisco", "Jueves, Viernes, Sábados", "Reggaetón", 18, "Fiestero"),
            ("La Tincho Fierro", "Jueves, Viernes, Sábados", "Reggaetón", 18, "Fiestero"),
            ("Niceto Club", "Jueves, Viernes, Sábados", "Pop, Electrónica, Funk, Reggaetón, Cumbia", 18, "Fiestero"),
            ("Crobar", "Jueves, Viernes, Sábados", "Techno, House, Electrónica", 18, "Under"),
            ("Under Club", "Viernes, Sábados", "Techno, Minimal", 18, "Under"),
            ("La Catedral Club", "Martes, Sábados", "Tango", 18, "Alternativo"),
            ("Amerika", "Viernes, Sábados, Domingos", "Pop, House, Electrónica", 18, "LGBTQ+"),
            ("Human Club", "Viernes, Sábados", "Pop, Electrónica, House, Reggaetón", 18, "LGBTQ+"),
            ("Contramano", "Sábados", "Dance, Pop Latino", 30, "LGBTQ+/Histórico"),
            ("Peuteo", "Viernes, Sábados", "Pop, Indie, Electrónica", 18, "LGBTQ+"),
            ("Club 69 @ Niceto", "Jueves", "Pop, Drag, Electrónica", 18, "LGBTQ+"),
            ("Banana Costanera", "Viernes, Sábados", "Pop , Reggaetón, electrónica", 18, "Fiestero")
        ]
        cursor.executemany("INSERT INTO boliches(nombre, dias, musica, edad_minima, perfil) VALUES (?,?,?,?,?)", boliches)
        conn.commit()
    conn.close()

def boliches_a_diccionario(filas):
    return [
        {
            "id": fila[0],
            "nombre": fila[1],
            "dias": fila[2],
            "musica": fila[3],
            "edad_minima": fila[4],
            "perfil": fila[5]
        } for fila in filas
    ]

def obtener_clima(ciudad):
    try:
        api_key = "21fa159658b0ace9fc40d85a615c4e7e"  # OpenWeatherMap API Key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={ciudad}&appid={api_key}&units=metric&lang=es"
        respuesta = requests.get(url)
        datos = respuesta.json()
        descripcion = datos["weather"][0]["description"]
        temperatura = datos["main"]["temp"]
        return f"Clima actual en {ciudad}: {descripcion}, {temperatura}°C"
    except:
        return "No se pudo obtener el clima."

def obtener_receta_afterparty():
    try:
        api_key = "fc0d1c4730b14d83b7f537d26e6e35a8"  # Configurá esta variable en tu entorno
        url = "https://api.spoonacular.com/recipes/random"
        params = {
            "apiKey": api_key,
            "number": 1,
            "tags": "quick, snack"
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            receta = data["recipes"][0]
            titulo = receta["title"]
            link = receta["sourceUrl"]
            return f"{titulo} - Más info: {link}"
        else:
            return "No se pudo obtener receta."
    except Exception as e:
        return f"Error obteniendo receta: {e}"

@app.route("/boliches", methods=["GET"])
def get_boliches():
    edad = int(request.args.get("edad", 0))
    musica = request.args.get("musica", "").lower()
    dia = request.args.get("dia", "").lower()

    clima_info = ""
    receta_info = ""

    if dia in ["viernes", "sábado"]:
        clima_info = obtener_clima("Buenos Aires")
        receta_info = obtener_receta_afterparty()

    conn = sqlite3.connect("base_datos.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM boliches
        WHERE edad_minima <= ?
        AND LOWER(musica) LIKE ?
        AND LOWER(dias) LIKE ?
    """, (edad, f"%{musica}%", f"%{dia}%"))
    resultados = cursor.fetchall()
    conn.close()

    return jsonify({
        "clima": clima_info,
        "receta_afterparty": receta_info,
        "resultados": boliches_a_diccionario(resultados)
    })

@app.route("/admin/boliches", methods=["GET"])
def ver_todos():
    conn = sqlite3.connect("base_datos.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM boliches")
    resultados = cursor.fetchall()
    conn.close()
    return jsonify(boliches_a_diccionario(resultados))

@app.route("/admin/boliches", methods=["POST"])
def agregar_boliche():
    datos = request.json
    conn = sqlite3.connect("base_datos.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO boliches(nombre, dias, musica, edad_minima, perfil) VALUES (?,?,?,?,?)",
                   (datos["nombre"], datos["dias"], datos["musica"], datos["edad_minima"], datos["perfil"]))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Boliche agregado correctamente."})

@app.route("/admin/boliches/<int:id>", methods=["PUT"])
def actualizar_boliche(id):
    datos = request.json
    conn = sqlite3.connect("base_datos.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE boliches SET nombre=?, dias=?, musica=?, edad_minima=?, perfil=? WHERE id=?",
                   (datos["nombre"], datos["dias"], datos["musica"], datos["edad_minima"], datos["perfil"], id))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Boliche actualizado correctamente."})

@app.route("/admin/boliches/<int:id>", methods=["DELETE"])
def eliminar_boliche(id):
    conn = sqlite3.connect("base_datos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM boliches WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return jsonify({"mensaje": "Boliche eliminado correctamente."})

@app.route("/admin/boliches/nombre/<string:nombre>", methods=["DELETE"])
def eliminar_por_nombre(nombre):
    conn = sqlite3.connect("base_datos.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM boliches WHERE LOWER(nombre) = LOWER(?)", (nombre,))
    conn.commit()
    eliminados = cursor.rowcount
    conn.close()
    if eliminados > 0:
        return jsonify({"mensaje": f"Se eliminó {eliminados} boliche(s) con nombre '{nombre}'."})
    else:
        return jsonify({"mensaje": f"No se encontró ningún boliche con nombre '{nombre}'."}), 404

if __name__ == "__main__":
    crear_base_si_no_existe()
    app.run(debug=True)
