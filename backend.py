import json
import os

# 1. Definición de Clases (POO)
class Material:
    def __init__(self, titulo: str, autor_subida: str, tipo: str, link_o_ruta: str, descripcion: str = ""):
        self.titulo = titulo
        self.autor_subida = autor_subida
        self.tipo = tipo  # 'Resumen', 'Guía', 'Prueba Anterior', 'Apunte'
        self.link_o_ruta = link_o_ruta
        self.descripcion = descripcion
        self.utilidad_votos = 0

    def votar_positivo(self):
        self.utilidad_votos += 1

    def a_diccionario(self):
        return {
            "titulo": self.titulo,
            "autor_subida": self.autor_subida,
            "tipo": self.tipo,
            "link_o_ruta": self.link_o_ruta,
            "descripcion": self.descripcion,
            "utilidad_votos": self.utilidad_votos
        }

    @classmethod
    def desde_diccionario(cls, datos):
        mat = cls(datos["titulo"], datos["autor_subida"], datos["tipo"], datos["link_o_ruta"], datos["descripcion"])
        mat.utilidad_votos = datos.get("utilidad_votos", 0)
        return mat


# 2. Estructura de Datos Jerárquica del Repositorio
class RepositorioFACSO:
    CARRERAS = [
        "Sociología", 
        "Psicología", 
        "Trabajo Social", 
        "Antropología", 
        "Educación Parvularia", 
        "Educación Física"
    ]

    def __init__(self, archivo_db="repositorio_data.json"):
        self.archivo_db = archivo_db
        # Diccionario anidado: {Carrera: {Año: {Semestre: {Asignatura: [Materiales]} } } }
        self.datos = {carrera: {} for carrera in self.CARRERAS}
        self.cargar_datos()

    def agregar_asignatura(self, carrera, ano, semestre, asignatura):
        if carrera in self.datos:
            if ano not in self.datos[carrera]:
                self.datos[carrera][ano] = {}
            if semestre not in self.datos[carrera][ano]:
                self.datos[carrera][ano][semestre] = {}
            if asignatura not in self.datos[carrera][ano][semestre]:
                self.datos[carrera][ano][semestre][asignatura] = []

    def subir_material(self, carrera, ano, semestre, asignatura, material: Material):
        try:
            self.agregar_asignatura(carrera, ano, semestre, asignatura)
            self.datos[carrera][ano][semestre][asignatura].append(material)
            self.guardar_datos()
            return True
        except KeyError as e:
            print(f"Error en la jerarquía del repositorio: {e}")
            return False

    def obtener_materiales(self, carrera, ano, semestre, asignatura):
        try:
            return self.datos[carrera][ano][semestre][asignatura]
        except KeyError:
            return []

    def guardar_datos(self):
        # Serialización a JSON
        datos_json = {}
        for c, anos in self.datos.items():
            datos_json[c] = {}
            for a, sems in anos.items():
                datos_json[c][a] = {}
                for s, asigs in sems.items():
                    datos_json[c][a][s] = {}
                    for asig, lista_mats in asigs.items():
                        datos_json[c][a][s][asig] = [m.a_diccionario() for m in lista_mats]
        
        with open(self.archivo_db, "w", encoding="utf8") as f:
            json.dump(datos_json, f, indent=4, ensure_ascii=False)

    def cargar_datos(self):
        if not os.path.exists(self.archivo_db):
            return
        try:
            with open(self.archivo_db, "r", encoding="utf8") as f:
                datos_json = json.load(f)
                for c, anos in datos_json.items():
                    for a, sems in anos.items():
                        for s, asigs in sems.items():
                            for asig, lista_mats in asigs.items():
                                self.agregar_asignatura(c, a, s, asig)
                                self.datos[c][a][s][asig] = [
                                    Material.desde_diccionario(m) for m in lista_mats
                                ]
        except Exception as e:
            print(f"No se pudieron cargar los datos guardados: {e}")


# 3. Interfaz de Usuario (Consola Interactiva)
def menu_principal():
    repo = RepositorioFACSO()
    
    # Datos de prueba iniciales si está vacío
    repo.subir_material(
        "Sociología", "1° Año", "Semestre 1", "Introducción a la Sociología",
        Material("Resumen Control 1 - Clasicos", "Estudiante_3er_Año", "Resumen", "https://link.com/apunte1", "Cubre Marx, Durkheim y Weber")
    )

    while True:
        print("\n=== REPOSITORIO ACADÉMICO FACSO ===")
        print("1. Ver material por Carrera / Año / Asignatura")
        print("2. Subir nuevo material")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            print("\nCarreras disponibles:")
            for idx, c in enumerate(repo.CARRERAS, 1):
                print(f"{idx}. {c}")
            
            try:
                c_idx = int(input("Seleccione carrera (número): ")) - 1
                carrera = repo.CARRERAS[c_idx]
                ano = input("Ingrese año (ej: 1° Año): ").strip()
                semestre = input("Ingrese semestre (ej: Semestre 1): ").strip()
                asignatura = input("Nombre de la asignatura: ").strip()

                materiales = repo.obtener_materiales(carrera, ano, semestre, asignatura)
                if not materiales:
                    print("\n--> No hay materiales registrados aún para esa asignatura.")
                else:
                    print(f"\n--- Materiales para {asignatura} ---")
                    for i, mat in enumerate(materiales, 1):
                        print(f"[{i}] {mat.titulo} ({mat.tipo}) - Subido por: {mat.autor_subida}")
                        print(f"    Descripción: {mat.descripcion}")
                        print(f"    Link/Ruta: {mat.link_o_ruta} | Votos utilidad: {mat.utilidad_votos}")
            except (ValueError, IndexError):
                print("Entrada inválida.")

        elif opcion == "2":
            print("\n--- Subir Material ---")
            for idx, c in enumerate(repo.CARRERAS, 1):
                print(f"{idx}. {c}")
            try:
                c_idx = int(input("Seleccione carrera (número): ")) - 1
                carrera = repo.CARRERAS[c_idx]
                ano = input("Año (ej: 1° Año): ").strip()
                semestre = input("Semestre (ej: Semestre 1): ").strip()
                asignatura = input("Asignatura: ").strip()
                titulo = input("Título del material: ").strip()
                autor = input("Tu nombre o apodo: ").strip()
                tipo = input("Tipo (Resumen/Guía/Prueba/Apunte): ").strip()
                link = input("Link o ruta del archivo: ").strip()
                desc = input("Descripción breve: ").strip()

                nuevo_mat = Material(titulo, autor, tipo, link, desc)
                if repo.subir_material(carrera, ano, semestre, asignatura, nuevo_mat):
                    print("\n¡Material subido y guardado con éxito!")
            except (ValueError, IndexError):
                print("Error en el ingreso de datos.")

        elif opcion == "3":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida.")

if __name__ == "__main__":
    menu_principal()