import json
import os

DB_FILE = "repositorio_data.json"

CARRERAS = [
    "Sociología",
    "Psicología",
    "Trabajo Social",
    "Antropología",
    "Educación Parvularia",
    "Educación Física"
]

ANOS = ["1° Año", "2° Año", "3° Año", "4° Año", "5° Año"]
SEMESTRES = ["Semestre 1", "Semestre 2"]

def cargar_datos():
    if not os.path.exists(DB_FILE):
        datos_demo = {
            "Sociología": {
                "1° Año": {
                    "Semestre 1": {
                        "Introducción a la Sociología": [
                            {
                                "titulo": "Resumen Control 1 - Clásicos",
                                "autor": "Estudiante_3er_Año",
                                "tipo": "Resumen",
                                "link": "https://drive.google.com/",
                                "descripcion": "Síntesis comentada de Marx, Durkheim y Weber.",
                                "votos": 12
                            }
                        ]
                    }
                }
            }
        }
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(datos_demo, f, indent=4, ensure_ascii=False)
        return datos_demo

    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def guardar_datos(datos):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

def agregar_material(db, carrera, ano, semestre, asignatura, nuevo_item):
    db.setdefault(carrera, {}).setdefault(ano, {}).setdefault(semestre, {}).setdefault(asignatura, [])
    db[carrera][ano][semestre][asignatura].append(nuevo_item)
    guardar_datos(db)