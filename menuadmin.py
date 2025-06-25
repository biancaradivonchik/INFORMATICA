import requests


BASE_URL = "http://127.0.0.1:5000/admin/boliches"


def ver_todos():
   response = requests.get(BASE_URL)
   if response.status_code == 200:
       boliches = response.json()
       if boliches:
           for b in boliches:
               print(f"ID: {b['id']}, Nombre: {b['nombre']}, Música: {b['musica']}, Días: {b['dias']}, Edad mínima: {b['edad_minima']}, Perfil: {b['perfil']}")
       else:
           print("No hay boliches en la base de datos.")
   else:
       print("Error al obtener los boliches.")


def agregar():
   nombre = input("Nombre: ")
   dias = input("Días (ej: Viernes, Sábados): ")
   musica = input("Música (ej: Reggaetón, Pop): ")
   edad = int(input("Edad mínima: "))
   perfil = input("Perfil (Fiestero, Under, etc.): ")


   data = {
       "nombre": nombre,
       "dias": dias,
       "musica": musica,
       "edad_minima": edad,
       "perfil": perfil
   }


   response = requests.post(BASE_URL, json=data)
   if response.status_code == 200:
       print("✅ Boliche agregado correctamente.")
   else:
       print("❌ Error al agregar el boliche.")


def modificar():
   id = input("ID del boliche a modificar: ")
   nombre = input("Nuevo nombre: ")
   dias = input("Nuevos días: ")
   musica = input("Nueva música: ")
   edad = int(input("Nueva edad mínima: "))
   perfil = input("Nuevo perfil: ")


   data = {
       "nombre": nombre,
       "dias": dias,
       "musica": musica,
       "edad_minima": edad,
       "perfil": perfil
   }


   response = requests.put(f"{BASE_URL}/{id}", json=data)
   if response.status_code == 200:
       print("✅ Boliche actualizado.")
   else:
       print("❌ Error al actualizar.")


def eliminar():
   id = input("ID del boliche a eliminar: ")
   response = requests.delete(f"{BASE_URL}/{id}")
   if response.status_code == 200:
       print("✅ Boliche eliminado.")
   else:
       print("❌ Error al eliminar.")


# Menú
def menu():
   while True:
       print("\n--- Menú Administrador Moodnight ---")
       print("1. Ver todos los boliches")
       print("2. Agregar un nuevo boliche")
       print("3. Modificar un boliche existente")
       print("4. Eliminar un boliche")
       print("5. Salir")
       opcion = input("Seleccioná una opción: ")


       if opcion == "1":
           ver_todos()
       elif opcion == "2":
           agregar()
       elif opcion == "3":
           modificar()
       elif opcion == "4":
           eliminar()
       elif opcion == "5":
           print("Saliendo...")
           break
       else:
           print("Opción inválida. Intentá de nuevo.")


if __name__ == "__main__":
   menu()
