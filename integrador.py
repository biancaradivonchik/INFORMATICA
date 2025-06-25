import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import sqlite3
from flask import Flask, jsonify, send_file, request

#FASE 1: Llamada a la API externa (requests + JSON) 

# 🔑 Tu API Key (reemplazá esto con tu clave real)
API_KEY = "RCL53toidGltKl9o8PbTjPQZzLjYRB0wARVHf82m" 
url = "https://api.data.gov/ed/collegescorecard/v1/schools"

# ⚙️ Parámetros para la consulta
params = {
    "api_key": API_KEY,
    "fields": "id,school.name,school.state,latest.student.size",
    "per_page": 20  #le dice a la API que no te devuelva todos los datos, sino solo los primeros 20 resultados.
    #le pedimos solo los primeros 20 porque eso nos dice el ejercicio
}

# la llama a la API
response = requests.get(url, params=params)
# hace la consulta a la api
#params = params, lo q hace es pedirle los parametros que nosotros escribimos a los parametros de la api

# pasamos la response a un JSON,
# si no ponemos [results], nos imprijme todo lo de la api, incluyendo info que no queremos
# results contiene la lista de universidades que es lo que nos interesa.
# es como un filtrado
data = response.json()["results"] 
# data contiene entonces, la lista de universidades
print(data)

#FASE 2:  Análisis de datos (Pandas) 

#Convertir los resultados en un DataFrame con Pandas 
df = pd.DataFrame(data)

df = df.dropna() #que me elimine las fulas del df que tiene al menos un valor nulo
df["latest.student.size"] = df["latest.student.size"].astype(int)
#convierte los valores de la columna en enteros, esto porque algunos pueden ser float o texto.

# PORQUE HACEMOS ESTO?
#por ahi puede haber errores cuando hacemos las estadisticas, entonces filtramos los valores nulos y los numericos los pasamos directamente a enteros.
print(df)

# Filtrar TOP 20 universidades más grandes

#● Guardar solo las 20 universidades con mayor cantidad de alumnos. 
df_top20 = df.sort_values("latest.student.size", ascending=False).head(20)
# creo la variable del df top 20, donde voy a tener solo las 20 universidades con la mayor Q de alumnos
# el df.sort_values lo que hace es agarrar el dataframe y ordenar la columna latest.student.size
# le ponemos ascending = FALSE, para que los ponga de mayor a menor.
# una vez que estan de mayor a menor, selecciono solo los primero 20, lo hago con .head(20)

#si quisiera los 20 ultimos uso .tall(y el numero)


#Exportar este subconjunto a un archivo .csv.
# df_top20.to_csv lo que hace es convertirlo en un archivo csv.
# le damos 1 parametros, nombre. al archivo csv le pusimos "universidades.csv"
# index = False, lo pusimos para que la columna del indicie no se repita.
df_top20.to_csv("universidades.csv", index = False)

#Y SI TUVIERAMOS QUE PASARLO A OTRO ARCHIVO Q NO SEA CSV?
# EXCEL --> df_top20.to_excel("universidades.xlsx", index=False)
# TXT --> df_top20.to_csv("universidades.txt", sep="\t", index=False) le ponemos sep para que para que cada columna quede separada y se lea mejor.


#ESTADISTICAS
#Cálculo del promedio de tamaño de las universidades TOP 20. 
promedio = df_top20["latest.student.size"].mean()
#Mayor cantidad de alumnos en el TOP 20 
maxUniversidad = df_top20["latest.student.size"].max()
#Menor cantidad de alumnos en el TOP 20
minUniversidad = df_top20["latest.student.size"].min()

#estadisticas extras de chat
# MEDIANA ---> mediana = df_top20["latest.student.size"].median()
# DESVIACION ESTANDAR ---> std_dev = df_top20["latest.student.size"].std()
# SUMA TOTAL DE ESTUDIANTES ---> total_estudiantes = df_top20["latest.student.size"].sum()
# CUANTAS UNIS HAY EN TOTAL ---> total_universidades = len(df)

#Calcular cuántas universidades ‘enormes’ existen (tienen más de 20.000 alumnos)
#creo una variable d las unis con mas de 20000
df_over20 = df[df["latest.student.size"]> 20000]
# esto me devuelve un nuevo df con las universidades con mas de 20.000 alumnos, pero lo que yo quiero es CUANTAS SON en numero

#AHI ME FILTRO LAS UNIVERSIDADES ENORMES, PERO ME PREGUNTA CUANTAS
#tenemos que contar cuantas hay ahora, uso LEN
# PORQUE USAMOS LEN? en este caso, len nos devuelve la CANTIDAD de filas en el df ya filtrado por las unis con mas de 20.000 
cantidad_over20 = len(df_over20)
print(cantidad_over20)

# EXTRA CHAT CON LEN- CONTAR CUANTAS UNIVERSIDADES HAY EN TOTAL
# total_universidades = len(df)

#LOC
# df.loc[filas, columnas], me sirve para seleccionar filas y columnas usando nombres o condiciones.
# usamos loc cuando querés filtrar filas por alguna condición y además elegir solo algunas columnas.
# por ejemplo, Si quiero filtrar las universidades con más de 20000 alumnos pero solo mostrar el nombre y estado (columnas específicas):
# df_over20_names_states = df.loc[df["latest.student.size"] > 20000, ["school.name", "school.state"]]
# Primer parámetro: condición para filas. Segundo parámetro: lista de columnas que quiero mostrar.

# POR QUE ACA NO USE LOC?
# no usamos porque solo pasamos un parametro (filas), y loc requiere 2.
# necesitabamos filtrar filas segun la condicion de que latest.student.size > 20000
# necesigtamos todas las columnas, por eso no las filtramos
#si diejra que necesita los mas d 20000 y algo mas, ahi si uso LOC

# OPCIONES DE FILTRADO
# filtrar unis con mas de 20.000 estudiantes ---> df_over20 = df[df["latest.student.size"] > 20000]
#  Filtrar por varias condiciones (AND). ej:unis con más de 20,000 est. y que estén en el estado "CA" ---> df_filtered = df[(df["latest.student.size"] > 20000) & (df["school.state"] == "CA")]
#  Filtrar por varias condiciones (OR). Ej: unis que tengan más de 30,000 estudiantes o que estén en el estado "NY" ---> df_filtered = df[(df["latest.student.size"] > 30000) | (df["school.state"] == "NY")]
# Filtrar con texto que contenga una palabra (string contains). ej: Uni cuyo nombre contenga "University" ---> df_filtered = df[df["school.name"].str.contains("University")]
#Filtrar filas con valores nulos o no nulos, por ejemplo en "latest.student.size" ---> df_filtered = df[df["latest.student.size"].notna()]
# Filtrar con rangos (between). ej: unis con q de estudiantes entre 10.000 y 30.000 ---> df_filtered = df[df["latest.student.size"].between(10000, 30000)]


#Realizar ciencia de datos, creando un archivo estadisticas.json, que contendrá:
#que contenga todo lo anterior q hicimos, las estadisticas
#nos pide un json asi que primero creamos el diccionario y guardarlo en json
#el diccionario va a tener todas las estadisticas
estadisticas = {
    "promedio_tamaño" : float(promedio),
    "universidad mayor tamaño" : int(maxUniversidad),
    "universidad menor tamaño" : int(minUniversidad),
    "cantidad mas de 20.000" : int(cantidad_over20)
}

#como lo guardamos en el json?
# abrimos un json, usamos with open
# esto crea un archivo JSON, w porque es modo escritura
# le ponemos as F, para que ese archivo se llame asi ahora, le asigna nombre F, puede ser cualquier nombre
with open ("estadisticas.json", "w") as f:
    json.dump(estadisticas,f)
#json.dump convierte un objeto de Python (como un diccionario o una lista) en formato JSON y lo escribe directamente en un archivo abierto
#JSONDUMP hace toma 2 cosas, primero el argumento que es estadisticas, y segundo el archivo donde vamos a escribir la info en formato json
#pasa las estadisticas a el archivo f

#antes de pasarlo a json, debo ver el tipo de dato que tengo, lo paso a uno que pueda leer phyton.
#paso el promedio a float, y lo demas a int
#hago esto porque al correrlo me dio error, entonces tengo que cmabiar el tipo de dato

#  Crear una visualización con un gráfico de barras de las 10 más grandes. Almacenar en “grafico.png” 

#grafico con el top 10
df_top10 = df.sort_values("latest.student.size", ascending=False).head(10)
#aca, hice lo mismo que antes para ver solo las 20, pero ahora le cambio a 10, ya que me pide solo las 10 mas grandes.

#LE DAMOS UN NUMERO A LA FIGURA, cambiamos el alto y el ancho
#le dijimos que el ancho y el alto sea 12 y 6
plt.figure(figsize = (12,6))  #ESTO LO DEBEMOS HACER AL INICIO

#llamo a plt y le digo que voy a hacer un grafico de barra
plt.bar(df_top10["school.name"], df_top10["latest.student.size"], color = "pink" )
# EJE X  = nombre de cada universidad
#EJE Y = cantidad de estudiantes actual 
#usamos un grafico de barras, en eje x muestra categorias y en eje y muestra valor numerico
#puse color para darle otro color

#TITULO AL GRAFICO
plt.title("TOP 10 UNIVERSIDADES")

#le dijimos que rote a 45° el eje x (los nombres), sino aparecen encimados.
plt.xticks(rotation=45)

#queremos tambien que no se vaya de la pantalla, le pedimos que lo ajuste a los bordes de la ventana
plt.tight_layout()

#le damos un titulo a el eje y
plt.ylabel ("Cantidad de estudiantes")

# guarda el gráfico que generaste como un archivo de imagen en tu computadora.
#nos va a servir despues para mostrarlo en postman
plt.savefig("grafico.png")

#ALMACENAMIENTO LOCAL:
#conectarse o crear la base de datos, si no existe se crea automaticamente
conn = sqlite3.connect("universidades.db")

# ponemos el cursor, lo usamos para enviar instrucciones a la SQL
cursor = conn.cursor()

#dentro de nuestro archivo recien creado vamos a crear la tabla universidades si no existe.
#vamos a poner los parametros de nuestra tabla, los elegimos nosotros
#a los parametros debemos indicarles el tipo de dato
cursor.execute("CREATE TABLE IF NOT EXISTS universidades(id INTEGER,name TEXT,state TEXT, size INTEGER)")

#control q va todo bien
print(df_top20)

for fila in df_top20.values:
    cursor.execute("INSERT INTO universidades (id, name, state, size) VALUES (?, ?, ?, ?)", (fila[3], fila[1], fila[2], fila[0]))
    print(fila)

# el dftop20.values te devuelve un arreglo tipo lista con los valores del dataframe pero sin los nombres de las columnas
#el for fila in dftop20 va a recorrer por cada una de esas filas
#  cursor.execute insert into universidad, le va a ir insertando los valores
#(fila[3], fila[1], fila[2], fila[0]), cada fila es el valor en la posicion dentro de la fila actual.
#fila[0] es el primer elemento de la fila, aca es ID, y asi.
# PORQUE PONEMOS FILA (fila[3], fila[1], fila[2], fila[0])? Y NO DIRECTAMENTE 0,1,2,3?
# porque en el dataframe que cree con la API que me dieron, el orden era asi 0 latest student, 1 name, 2 state y 3 id
# y en mi tabla sql al insertar los valores id,name,state y size, tengo que ordenarlos. 
# cuando cree mi tabla puse ID, NAME, STATE Y SIZE. por lo que para insertar los valores, tengo que hacerlo de manera ordenada.
# SI NO ORDENO BIEN LAS FILAS, un valor se me puede guardar en otra variable.
# entonces yo ya se que posicion tiene cada elemento porque lo vi en el data frame q me dieron.
# con eso ordeno e inserto los valores ordenados, entonces quedaria asi:
# id, name, state, size ---> fila[3], fila [1], fila[2], fila[0]

#la estructura de cada fila es: [fila[0] = size, fila[1] = name, fila[2] = state, fila[3] = id]
# y la tabla que cree es (id, name, state, size)
# por eso hay que reordenar antes de insertar

#guardar los cambios
conn.commit()

#termina la conexion
conn.close()


#FASE 4 ENDOPOINTS CON FLASK
#importo el flask con el jsonify
#tenemos q crear la API
app = Flask(__name__)
#creamos la aplicacion flask, esto nos permite crear nuestra API

# PRIMER ENDPOINT GET, Lista todas las universidades almacenadas.
@app.route("/universidades", methods = ["GET"]) # generamos la ruta del servidor, importante poner el methods
def listar_universidades(): #definimos la funcion que se ejecuta cuando el servidor accede a /universidades
    
    conn = sqlite3.connect("universidades.db") # lo conectamos con la base de datos para poder hacer las consultas
    # solo en este endpoint nos conectamos a la base de datos, ya que necesitamos leer esos datos almacenados.
    # los demas endpoints usan cosas que creamos en este codigo, como el grafico y las estadisticas

    todas_filas = conn.execute("SELECT * FROM universidades").fetchall()
    #con conn.execute consulta la base de datos, y con fetchall obtiene todos los resultados
    #fetchall Recorre todos los resultados y los convierte en una lista de tuplas, donde cada tupla representa una fila de la tabla.
    # con la variable creada todas_filas, la usamos apra recorrer por fila con for
    
    conn.close()
#debemos cerrar la conexion

    universidades = []
    for fila in todas_filas:
    # usamos un for para recorrer las filas porque fetchall nos da una lista de tuplas
    # pero flask no puede devolver directamente un json, porque la tupla no tiene nombre, solo posiciones.
    #Por eso tenés que recorrer cada fila y transformarla en un diccionario,
    # POR QUE LAS GUARDAMOS EN DICCIONARISO?
    #Porque el formato JSON, que usa Flask para devolver los datos al navegador o a otro sistema, funciona con diccionarios
        #voy a crear un diccionario para guardar todas las filas
        uni = {
            "id" : fila[0],
            "name": fila[1],
            "state": fila[2],
            "size" : fila[3]
        }
        # ponemos fila 0, fila 2...  porque cada fila es una tupla, y las posiciones indican a qué dato estás accediendo.
        # EL ORDEN DE LA FILA, LO DEFINE MI TABLA SQL
        universidades.append(uni) # aca agrego mi diccinario uni a la lista universidades.
    return jsonify(universidades) # convierte estructuras de python en json
#convierte mi diccionario en json
#Ese JSON es lo que la API devuelve cuando el usuario accede a /universidades

# SEGUNDO ENDPOINT GET /grafico - Devuelve nuestra visualización creada durante el análisis. 
@app.route("/grafico", methods=["GET"]) # generamos la ruta del servidor, ponemos el metodo correcto
def get_grafico(): # creamos la funcion a ejecutar para el servidor cuando ponga /grafico
    return send_file("grafico.png") # usamos la libreria send_file, que nos devuelve el grafico creado. 
#debemos dentro ponerle el nombre del grafico que hicimos. esta en plt.savefig(nombre)

#TERCER ENDPOINT GET /estadisticas - Muestra el JSON con las estadísticas calculadas 
# YA HABIAMOS CALCULADO LAS ESTADISTICAS Y LAS HABIAMOS PUESTO EN UN ARCHIVO JSON
@app.route("/estadisticas", methods=["GET"]) # definimos la ruta sel servidor
def mostrar_estadisticas(): # creamos la funcion a ejecutar
    
    #como estan en un json que ya creamos, las tenemos que pasar
    # abrimos el archivo estadisticas.json para leerlo
    with open ("estadisticas.json") as f:
        datos = json.load(f)
#JSON LOAD devuelve el contenido json convertido a un objeto phyton
# de json lo pasamos a phyton para manipular los datos, pero los datos el servidor los va a tener que leer como un json, entonces lo pasamos a json d nuevo
# solo lo pasa a phyton d nuevo para poder trabajar con los datos dentro del codigo.
    return jsonify(datos) # Convertimos ese diccionario a JSON para devolverlo en la respuesta HTTP


# MAS ENDPOINTS CHAT

@app.route("/universidades/buscar", methods=["GET"])
def buscar_por_nombre():
    nombre = request.args.get("nombre", "")  #request.args permite acceder a los parámetros que vienen en la URL
    #.get("nombre", "") busca el parámetro nombre. Si no lo encuentra, usa "" (cadena vacía).

    conn = sqlite3.connect("universidades.db")
#Abre una conexión a la base de datos llamada universidades.db.

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM universidades WHERE name LIKE ?", ('%' + nombre + '%',))
    #una consulta SQL para buscar en la tabla universidades todas las filas donde la columna name contenga la palabra nombr
    # El símbolo % es un comodín que significa "cualquier cosa antes o después".
# el signo ?, se reemplaza por ese valor, pero de forma segura (para evitar inyecciones SQL).

    filas = cursor.fetchall() #Guarda todas las filas que devolvió la consulta en una lista llamada filas.
    conn.close()

    universidades = []
    for fila in filas:
        uni = {
            "id": fila[0],
            "name": fila[1],
            "state": fila[2],
            "size": fila[3]
        }
        universidades.append(uni)

    return jsonify(universidades)
# COMO LO USO EN POSTMAN?
# http://127.0.0.1:4000/universidades/buscar?nombre=(ACA PONEMOS EL NOMBRE A BUSCAR)


if __name__ == "__main__":
    app.run(debug = True, port = 4000)
    # esto arranca el servidor flask que creamos
    # debug=True: Activa el modo depuración, que permite que el servidor se reinicie automáticamente si hacés cambios en el código 
    # port=4000: Especifica en qué puerto se va a ejecutar tu servidor Flask.