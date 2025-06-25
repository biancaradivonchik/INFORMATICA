import requests

# URL de la API para obtener una imagen aleatoria de perro
url = "https://dog.ceo/api/breeds/image/random"

try:
    # Llamada a la API
    response = requests.get(url)

    # Verificamos si la respuesta fue exitosa (código 200)
    if response.status_code == 200:
        data = response.json()  # Convertimos la respuesta en un diccionario
        imagen_url = data.get("message")  # Obtenemos la URL de la imagen

        # Guardamos la URL en el archivo imagen_perro.txt
        with open("imagen_perro.txt", "w") as archivo:
            archivo.write(imagen_url)
    else:
        # Si la API responde pero con error (ej. 404, 500)
        with open("imagen_perro.txt", "w") as archivo:
            archivo.write("Error al conectar con la API")
except:
    # Si hubo un error de conexión, como que no hay internet
    with open("imagen_perro.txt", "w") as archivo:
        archivo.write("Error al conectar con la API")
