import requests

print("🌙 Bienvenido a Moodnight 🌙🍸\n")
edad = int(input("👤 Ingresá tu edad: "))
musica = input("🎶 ¿Qué tipo de música te gusta?: ")
dia = input("📅 ¿Qué día querés salir? (ej: Viernes): ")

params = {
    "edad": edad,
    "musica": musica,
    "dia": dia
}

try:
    response = requests.get("http://127.0.0.1:5000/boliches", params=params)
    if response.status_code == 200:
        data = response.json()

        # Mostrar clima si hay
        clima = data.get("clima", "")
        if clima:
            print("\n🌤️ " + clima)

        print("\n🎧 Buscando boliches que se ajusten a tu mood...\n")
        if data["resultados"]:
            print("🎉 Boliches recomendados para vos:\n")
            for boliche in data["resultados"]:
                print(f"🔸 {boliche['nombre']} - {boliche['musica']} - {boliche['dias']}")
        else:
            print("😕 No encontramos boliches con esas características.")

        # Mostrar recomendación de receta si hay
        receta = data.get("receta_afterparty", "")
        if receta:
            print("\n🍴 Y para el bajón del after, te recomendamos esta receta rápida y fácil:")
            print(f"👉 {receta}")

    else:
        print("❌ Error al conectar con la API.")
except Exception as e:
    print("⚠️ Error:", e)
