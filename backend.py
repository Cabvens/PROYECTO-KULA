import json
import os

DB_FILE = "repositorio_data.json"
UPLOADS_DIR = "uploads"

# Crear carpeta de subidas si no existe
os.makedirs(UPLOADS_DIR, exist_ok=True)

SEMESTRES_POR_ANO = {
    "1° Año": ["Semestre 1", "Semestre 2"],
    "2° Año": ["Semestre 3", "Semestre 4"],
    "3° Año": ["Semestre 5", "Semestre 6"],
    "4° Año": ["Semestre 7", "Semestre 8"],
    "5° Año": ["Semestre 9", "Semestre 10"]
}

MALLA_CURRICULAR = {
    "Sociología": {
        "1° Año": {
            "Semestre 1": [
                "Filosofía Social",
                "Historia de la Sociedad Moderna",
                "Introducción a la Sociología",
                "Antropología",
                "Psicología Social",
                "Inglés I",
                "CFT"
            ],
            "Semestre 2": [
                "Teoría Sociológica Clásica",
                "Historia Social de América Latina",
                "Epistemología",
                "Diseño de Investigación",
                "Población y Sociedad",
                "Inglés II"
            ]
        },
        "2° Año": {
            "Semestre 3": [
                "Teorías Sociológicas de la Sociedad Moderna",
                "Historia Social de Chile",
                "Estrategias de Investigación Cualitativa",
                "Estadística Descriptiva",
                "Economía",
                "Inglés III",
                "Deportivo/Artístico"
            ],
            "Semestre 4": [
                "Teorías Sociológicas Contemporáneas",
                "Sociología Política",
                "Análisis de Investigación Cualitativa",
                "Estadística Correlacional",
                "Estrategias de Investigación Cuantitativa",
                "Inglés IV",
                "CFT"
            ]
        },
        "3° Año": {
            "Semestre 5": [
                "Desigualdades y Estratificación Social",
                "Sociología de la Cultura",
                "Sociología del Género",
                "Estadística Multivariada",
                "Electivo",
                "CFG o Deportivo/Artístico"
            ],
            "Semestre 6": [
                "Teoría y Sociedad Latinoamericana",
                "Sociología Económica",
                "Sociología de las Políticas Públicas",
                "Electivo"
            ]
        },
        "4° Año": {
            "Semestre 7": [
                "Transformaciones Sociales del Chile Contemporáneo",
                "Investigación Evaluativa",
                "Electivo"
            ],
            "Semestre 8": [
                "Seminario de Grado",
                "Electivo"
            ]
        },
        "5° Año": {
            "Semestre 9": ["Seminario de Título I"],
            "Semestre 10": ["Seminario de Título II", "Práctica Profesional"]
        }
    },
    "Trabajo Social": {
        "1° Año": {
            "Semestre 1": [
                "Fundamentos Históricos y Políticos del Trabajo Social",
                "Filosofía",
                "Historia Social Contemporánea",
                "Teoría Sociológica I",
                "Metodología de la Investigación Social I",
                "Inglés I",
                "Curso Transversal de Facultad"
            ],
            "Semestre 2": [
                "Enfoques Críticos en Trabajo Social",
                "Estado y Sociedad Contemporánea",
                "Historia Social de Chile",
                "Teoría Sociológica II",
                "Estadística I",
                "Inglés II",
                "Curso de Formación General"
            ]
        },
        "2° Año": {
            "Semestre 3": [
                "Justicia Social, Derechos y Ciudadanía",
                "Epistemología de las Ciencias Sociales",
                "Psicología",
                "Economía I",
                "Estadística II",
                "Inglés III",
                "Curso Deportivo/Artístico"
            ],
            "Semestre 4": [
                "Fundamentos de la Intervención Social",
                "Ética Social",
                "Antropología",
                "Economía II",
                "Metodología de la Investigación Social II",
                "Inglés IV",
                "Curso Transversal de Facultad"
            ]
        },
        "3° Año": {
            "Semestre 5": [
                "Núcleo I+D Disciplinario I",
                "Núcleo Temático I+D Electivo",
                "Indicadores Sociales",
                "Políticas Sociales",
                "Metodología de la Investigación Social III"
            ],
            "Semestre 6": [
                "Núcleo I+D Disciplinario II",
                "Intervención en Fenómenos Sociales Extremos",
                "Núcleo Temático I+D Electivo",
                "Sustentabilidad de Impacto Social",
                "Planificación y Gestión Social",
                "Normativas Jurídicas de la Intervención Social"
            ]
        },
        "4° Año": {
            "Semestre 7": [
                "Núcleo I+D Disciplinario III",
                "Cuestión Social y Desigualdades",
                "Sujetos y Movimientos Sociales",
                "Análisis Comparados de Políticas Sociales",
                "Análisis Social del Territorio"
            ],
            "Semestre 8": [
                "Núcleo I+D Disciplinario IV",
                "Cosmopolitismo, Diversidad e Intervención Social",
                "Teorías de Género",
                "Evaluación Social de Programas y Proyectos",
                "Innovación Social y Transferencia"
            ]
        },
        "5° Año": {
            "Semestre 9": ["Núcleo de Titulación I+D I", "Asignatura Diplomado o Magíster"],
            "Semestre 10": ["Núcleo de Titulación I+D II", "Asignatura Diplomado o Magíster"]
        }
    },
    "Psicología": {
        "1° Año": {
            "Semestre 1": [
                "Filosofía",
                "Psicología",
                "Métodos de la Investigación Social",
                "Historia Social de Chile",
                "Psicobiología",
                "Curso Transversal FACSO I",
                "Inglés I"
            ],
            "Semestre 2": [
                "Epistemología de las Ciencias Sociales",
                "Psicología de la Personalidad",
                "Procesos Psicológicos Básicos",
                "Estadística I",
                "Procesos Básicos de Aprendizaje",
                "CFG",
                "Inglés II"
            ]
        },
        "2° Año": {
            "Semestre 3": [
                "Teorías y Sistemas Psicológicos",
                "Psicopatología",
                "Psicología del Desarrollo I",
                "Estadística II",
                "Psicología Social I",
                "Neurofisiología",
                "Curso Transversal FACSO II",
                "Inglés III"
            ],
            "Semestre 4": [
                "Introducción a la Evaluación Psicológica",
                "Psiquiatría",
                "Psicología del Desarrollo II",
                "Metodología Cualitativa",
                "Psicología Social II",
                "Neurociencia Cognitiva",
                "Curso Artístico/Deportivo",
                "Inglés IV"
            ]
        },
        "3° Año": {
            "Semestre 5": [
                "Psicología del Trabajo y las Organizaciones",
                "Psicología Clínica",
                "Psicología Educacional",
                "Psicología Jurídica",
                "Psicología Comunitaria"
            ],
            "Semestre 6": ["Cursos Optativos", "Curso Transversal FACSO III"]
        },
        "4° Año": {
            "Semestre 7": ["Seminario de Grado I", "Cursos Optativos", "Curso Transversal FACSO IV"],
            "Semestre 8": ["Seminario de Grado II", "Cursos Optativos"]
        },
        "5° Año": {
            "Semestre 9": ["Práctica Profesional I", "Seminario de Práctica I", "Formación Profesional"],
            "Semestre 10": ["Práctica Profesional II", "Seminario de Práctica II", "Formación Profesional"]
        }
    },
    "Antropología (Social)": {
        "1° Año": {
            "Semestre 1": [
                "Evolución Humana",
                "Formación de la Sociedad Moderna",
                "Problemas Fundamentales de la Antropología I",
                "Filosofía de las Ciencias Sociales",
                "Taller I",
                "Curso Transversal de Facultad",
                "Inglés I"
            ],
            "Semestre 2": [
                "Cazadores Recolectores",
                "Formación de la Sociedad Chilena",
                "Problemas Fundamentales de la Antropología II",
                "Teoría Social",
                "Taller II",
                "Deportivo/Artístico Cultural",
                "Inglés II"
            ]
        },
        "2° Año": {
            "Semestre 3": [
                "Sociedades Complejas",
                "Problemas Contemporáneos de la Antropología",
                "Problemas Fundamentales de la Antropología III",
                "Estadística I",
                "Taller III",
                "CFG",
                "Inglés III"
            ],
            "Semestre 4": [
                "Electivo de Especialización",
                "Problemas Fundamentales de la Antropología IV",
                "Estadística II",
                "Taller IV",
                "Curso Transversal de Facultad",
                "Inglés IV"
            ]
        },
        "3° Año": {
            "Semestre 5": [
                "Etnologías y Estudios Interculturales I",
                "Problemas Teóricos en Antropología Social I",
                "Taller de Investigación Social Aplicada",
                "Antropologías Aplicadas I",
                "Métodos y Técnicas de Investigación Social I",
                "Curso Complementario I"
            ],
            "Semestre 6": [
                "Etnologías y Estudios Interculturales II",
                "Problemas Teóricos en Antropología Social II",
                "Taller de Integración",
                "Antropologías Aplicadas II",
                "Métodos y Técnicas de Investigación Social II",
                "Curso Complementario II"
            ]
        },
        "4° Año": {
            "Semestre 7": [
                "Etnologías y Estudios Interculturales III",
                "Problemas Teóricos en Antropología Social III",
                "Taller de Investigación I",
                "Antropologías Aplicadas III",
                "Métodos y Técnicas de Investigación Social III",
                "Curso Complementario III"
            ],
            "Semestre 8": [
                "Problemas Contemporáneos",
                "Problemas Teóricos en Antropología Social IV",
                "Taller de Investigación II",
                "Antropologías Aplicadas IV",
                "Métodos y Técnicas de Investigación Social IV",
                "Curso Complementario IV"
            ]
        },
        "5° Año": {
            "Semestre 9": ["Taller de Memoria I", "Práctica Profesional"],
            "Semestre 10": ["Taller de Memoria II"]
        }
    },
    "Antropología (Arqueología)": {
        "1° Año": {
            "Semestre 1": [
                "Evolución Humana",
                "Formación de la Sociedad Moderna",
                "Problemas Fundamentales de la Antropología I",
                "Filosofía de las Ciencias Sociales",
                "Taller I",
                "Curso Transversal de Facultad",
                "Inglés I"
            ],
            "Semestre 2": [
                "Cazadores Recolectores",
                "Formación de la Sociedad Chilena",
                "Problemas Fundamentales de la Antropología II",
                "Teoría Social",
                "Taller II",
                "Deportivo/Artístico Cultural",
                "Inglés II"
            ]
        },
        "2° Año": {
            "Semestre 3": [
                "Sociedades Complejas",
                "Problemas Contemporáneos de la Antropología",
                "Problemas Fundamentales de la Antropología III",
                "Estadística I",
                "Taller III",
                "CFG",
                "Inglés III"
            ],
            "Semestre 4": [
                "Electivo de Especialización",
                "Problemas Fundamentales de la Antropología IV",
                "Estadística II",
                "Taller IV",
                "Curso Transversal de Facultad",
                "Inglés IV"
            ]
        },
        "3° Año": {
            "Semestre 5": [
                "Etnologías y Estudios Interculturales I",
                "Teoría Arqueológica I",
                "Problemas de Prehistoria I",
                "Laboratorio I",
                "Manejo de Colecciones",
                "Taller de Investigación Social Aplicada"
            ],
            "Semestre 6": [
                "Etnologías y Estudios Interculturales II",
                "Teoría Arqueológica II",
                "Problemas de Prehistoria II",
                "Laboratorio II",
                "Laboratorio III",
                "Métodos y Técnicas de Terreno I",
                "Taller de Arqueología Cuantitativa"
            ]
        },
        "4° Año": {
            "Semestre 7": [
                "Etnologías y Estudios Interculturales III",
                "Teoría Arqueológica III",
                "Problemas de Prehistoria III",
                "Laboratorio IV",
                "Laboratorio V",
                "Métodos y Técnicas de Terreno II",
                "Taller de Investigación I"
            ],
            "Semestre 8": [
                "Problemas Contemporáneos",
                "Teoría Arqueológica IV",
                "Problemas de Prehistoria IV",
                "Arqueología Aplicada al Patrimonio",
                "Métodos y Técnicas de Terreno III",
                "Métodos y Técnicas de Terreno IV",
                "Taller de Investigación II"
            ]
        },
        "5° Año": {
            "Semestre 9": ["Taller de Memoria I", "Práctica Profesional"],
            "Semestre 10": ["Taller de Memoria II"]
        }
    },
    "Antropología (Física)": {
        "1° Año": {
            "Semestre 1": [
                "Evolución Humana",
                "Formación de la Sociedad Moderna",
                "Problemas Fundamentales de la Antropología I",
                "Filosofía de las Ciencias Sociales",
                "Taller I",
                "Curso Transversal de Facultad",
                "Inglés I"
            ],
            "Semestre 2": [
                "Cazadores Recolectores",
                "Formación de la Sociedad Chilena",
                "Problemas Fundamentales de la Antropología II",
                "Teoría Social",
                "Taller II",
                "Deportivo/Artístico Cultural",
                "Inglés II"
            ]
        },
        "2° Año": {
            "Semestre 3": [
                "Sociedades Complejas",
                "Problemas Contemporáneos de la Antropología",
                "Problemas Fundamentales de la Antropología III",
                "Estadística I",
                "Taller III",
                "CFG",
                "Inglés III"
            ],
            "Semestre 4": [
                "Electivo de Especialización",
                "Problemas Fundamentales de la Antropología IV",
                "Estadística II",
                "Taller IV",
                "Curso Transversal de Facultad",
                "Inglés IV"
            ]
        },
        "3° Año": {
            "Semestre 5": [
                "Etnologías y Estudios Interculturales I",
                "Teoría Antropología Biológica I",
                "Método Antropología Biológica I",
                "Bioarqueología",
                "Anatomía",
                "Taller de Investigación Social Aplicada"
            ],
            "Semestre 6": [
                "Etnologías y Estudios Interculturales II",
                "Teoría Antropología Biológica II",
                "Método Antropología Biológica II",
                "Paleopatología",
                "Histología",
                "Taller de Estadística para Antropología Física"
            ]
        },
        "4° Año": {
            "Semestre 7": [
                "Etnologías y Estudios Interculturales III",
                "Teoría Antropología Biológica III",
                "Método Antropología Biológica III",
                "Antropología Forense",
                "Fisiología",
                "Taller de Investigación I"
            ],
            "Semestre 8": [
                "Problemas Contemporáneos",
                "Teoría Antropología Biológica IV",
                "Método Antropología Biológica IV",
                "Paleantropología",
                "Crecimiento, Desarrollo y Nutrición",
                "Taller de Investigación II"
            ]
        },
        "5° Año": {
            "Semestre 9": ["Taller de Memoria I", "Práctica Profesional"],
            "Semestre 10": ["Taller de Memoria II"]
        }
    },
    "Pedagogía en Educación Especial": {
        "1° Año": {
            "Semestre 1": [
                "Historia y Fundamentos de la Educación",
                "Práctica 1: Introducción al Sistema Educativo Chileno",
                "Fundamentos de la Educación Inclusiva",
                "Desarrollo, Cognición y Aprendizaje",
                "Construcciones Sociales de las Infancias y Juventudes",
                "CTF Desarrollo de Habilidades Comunicativas"
            ],
            "Semestre 2": [
                "Epistemología y Educación",
                "Práctica 2: Introducción al Campo Profesional",
                "Expresión Artística, Juego y Creatividad",
                "Desarrollo Psicolingüístico en Contextos de Diversidad",
                "CTF Género y Ciencias Sociales",
                "Lengua de Señas Chilena"
            ]
        },
        "2° Año": {
            "Semestre 3": [
                "Pedagogía de la Diversidad e Inclusión",
                "Práctica 3: Educación Inclusiva en Primera Infancia",
                "Psicomotricidad y Diversidad",
                "Inclusión en Discapacidad Intelectual",
                "Curso Formación General",
                "Inglés I"
            ],
            "Semestre 4": [
                "Currículum y Didáctica",
                "Práctica 4: Educación Básica e Inclusión",
                "Didáctica del Lenguaje en Contextos de Diversidad",
                "Evaluación para la Diversidad",
                "Curso Deportivo o Artístico",
                "Inglés II"
            ]
        }
    },
    "Pedagogía en Educación Física": {
        "1° Año": {
            "Semestre 1": [
                "Historia y Fundamentos de la Educación",
                "Práctica 1: Introducción al Sistema Educativo Chileno",
                "Anatomía Humana Aplicada",
                "Bases de la Educación Física y Lamotricidad Humana",
                "Construcciones Sociales de las Infancias y Juventudes",
                "CTF Desarrollo de Habilidades Comunicativas"
            ],
            "Semestre 2": [
                "Epistemología de la Educación",
                "Práctica 2: Introducción al Campo Profesional",
                "Fisiología General",
                "Deportes Individuales 1",
                "CTF Género y Ciencias Sociales",
                "Lengua de Señas Chilena"
            ]
        }
    },
    "Pedagogía en Educación Parvularia": {
        "1° Año": {
            "Semestre 1": [
                "Bases del Desarrollo y Aprendizaje",
                "Construcciones Sociales sobre la Infancia",
                "Historia y Fundamentos de la Educación",
                "Salud y Cuidado del Niño",
                "Filosofía y Epistemología de las Ciencias Sociales",
                "Práctica 1: Aproximaciones al Campo Profesional"
            ],
            "Semestre 2": [
                "Teorías del Desarrollo y Aprendizaje",
                "Metodología de la Investigación",
                "Pedagogía de la Diversidad e Inclusión Social",
                "Currículum y Didáctica en la EP",
                "Familia, Comunidad y Territorio",
                "Práctica 2: Aproximaciones al Quehacer Pedagógico"
            ]
        }
    }
}

CARRERAS = list(MALLA_CURRICULAR.keys())
ANOS = ["1° Año", "2° Año", "3° Año", "4° Año", "5° Año"]

def obtener_semestres_por_ano(ano):
    return SEMESTRES_POR_ANO.get(ano, ["Semestre 1", "Semestre 2"])

def obtener_ramos_oficiales(carrera, ano, semestre):
    return MALLA_CURRICULAR.get(carrera, {}).get(ano, {}).get(semestre, [])

def guardar_archivo_local(uploaded_file):
    """Guarda un archivo subido por el usuario en el directorio uploads/."""
    if uploaded_file is None:
        return None
    
    nombre_seguro = uploaded_file.name.replace(" ", "_")
    ruta_destino = os.path.join(UPLOADS_DIR, nombre_seguro)
    
    with open(ruta_destino, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    return ruta_destino

def cargar_datos():
    if not os.path.exists(DB_FILE):
        datos_demo = {
            "Sociología": {
                "1° Año": {
                    "Semestre 1": {
                        "Introducción a la Sociología": [
                            {
                                "titulo": "Resumen Control 1 - Clásicos de la Sociología",
                                "autor": "Estudiante_3er_Año",
                                "tipo": "Resumen",
                                "link": "https://drive.google.com/",
                                "descripcion": "Síntesis comentada sobre Marx, Durkheim y Weber.",
                                "votos": 12,
                                "calificaciones": [5, 4, 5]
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
    if "calificaciones" not in nuevo_item:
        nuevo_item["calificaciones"] = []
    db[carrera][ano][semestre][asignatura].append(nuevo_item)
    guardar_datos(db)

def agregar_calificacion(db, carrera, ano, semestre, asignatura, index, nota):
    try:
        item = db[carrera][ano][semestre][asignatura][index]
        if "calificaciones" not in item:
            item["calificaciones"] = []
        item["calificaciones"].append(int(nota))
        guardar_datos(db)
        return True
    except (KeyError, IndexError):
        return False

