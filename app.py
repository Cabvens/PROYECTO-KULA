import streamlit as st
from backend import CARRERAS, ANOS, SEMESTRES, cargar_datos, guardar_datos, agregar_material

st.set_page_config(page_title="Proyecto Andamio", page_icon="📚", layout="wide")

if "db" not in st.session_state:
    st.session_state.db = cargar_datos()

st.title("📚 Proyecto Andamio: Repositorio Académico FACSO")

# Navegación lateral
st.sidebar.header("🎯 Filtros")
carrera_sel = st.sidebar.selectbox("Carrera", CARRERAS)
ano_sel = st.sidebar.selectbox("Año", ANOS)
semestre_sel = st.sidebar.selectbox("Semestre", SEMESTRES)

tab_explorar, tab_subir = st.tabs(["🔍 Explorar Materiales", "📤 Aportar Material"])

with tab_explorar:
    carrera_dict = st.session_state.db.get(carrera_sel, {}).get(ano_sel, {}).get(semestre_sel, {})
    asignaturas = list(carrera_dict.keys())

    if not asignaturas:
        st.info("No hay asignaturas registradas en esta sección aún.")
    else:
        asig_sel = st.selectbox("Asignatura:", asignaturas)
        materiales = carrera_dict.get(asig_sel, [])
        
        for idx, item in enumerate(materiales):
            with st.container(border=True):
                st.markdown(f"#### 📄 {item['titulo']}")
                st.write(item["descripcion"])
                st.markdown(f"🔗 [Acceder al enlace]({item['link']}) | 👍 Votos: {item['votos']}")
                if st.button("Votar útil", key=f"voto_{idx}"):
                    item["votos"] += 1
                    guardar_datos(st.session_state.db)
                    st.rerun()

with tab_subir:
    with st.form("form_subir"):
        asig = st.text_input("Asignatura")
        titulo = st.text_input("Título del Material")
        tipo = st.selectbox("Tipo", ["Resumen", "Guía", "Prueba", "Apunte"])
        autor = st.text_input("Tu Nombre/Apodo", value="Anónimo")
        link = st.text_input("Link al archivo")
        desc = st.text_area("Descripción")
        
        if st.form_submit_button("Publicar"):
            if asig and titulo and link:
                nuevo = {"titulo": titulo, "autor": autor, "tipo": tipo, "link": link, "descripcion": desc, "votos": 0}
                agregar_material(st.session_state.db, carrera_sel, ano_sel, semestre_sel, asig, nuevo)
                st.success("¡Material guardado!")
                st.rerun()