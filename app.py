import streamlit as st
from backend import (
    CARRERAS,
    ANOS,
    SEMESTRES,
    cargar_datos,
    guardar_datos,
    agregar_material
)

st.set_page_config(page_title="Proyecto Kula", page_icon="📚", layout="wide")

if "db" not in st.session_state:
    st.session_state.db = cargar_datos()

st.title("📚 Repositorio de materiales de estudio")
st.caption("Plataforma de colaboración y transmisión de conocimientos entre pares.")

# Navegación lateral
st.sidebar.header("🎯 Ingrese su estado académico")
carrera_sel = st.sidebar.selectbox("Carrera", CARRERAS)
ano_sel = st.sidebar.selectbox("Año", ANOS)
semestre_sel = st.sidebar.selectbox("Semestre", SEMESTRES)

tab_explorar, tab_subir = st.tabs(["🔍 Explorar Materiales", "📤 Aportar Material"])

# ------------------------------------------------------------------------------
# TAB 1: EXPLORAR MATERIALES
# ------------------------------------------------------------------------------
with tab_explorar:
    st.subheader(f"Navegando: {carrera_sel} > {ano_sel} > {semestre_sel}")
    carrera_dict = st.session_state.db.get(carrera_sel, {}).get(ano_sel, {}).get(semestre_sel, {})
    asignaturas = list(carrera_dict.keys())

    if not asignaturas:
        st.info("💡 No hay asignaturas registradas en esta sección aún")
    else:
        asig_sel = st.selectbox("Selecciona Asignatura:", asignaturas)
        materiales = carrera_dict.get(asig_sel, [])
        
        st.markdown(f"### Materiales para **{asig_sel}** ({len(materiales)})")
        
        for idx, item in enumerate(materiales):
            with st.container(border=True):
                col1, col2 = st.columns([4, 1])
                with col1:
                    st.markdown(f"#### 📄 {item['titulo']}")
                    st.markdown(f"**Tipo:** `{item['tipo']}` | **Aportado por:** _{item['autor']}_")
                    st.write(item["descripcion"])
                    st.markdown(f"🔗 [Acceder al enlace]({item['link']})")
                with col2:
                    st.metric(label="Utilidad", value=f"👍 {item['votos']}")
                    if st.button("Votar útil", key=f"voto_{asig_sel}_{idx}"):
                        item["votos"] += 1
                        guardar_datos(st.session_state.db)
                        st.rerun()

# ------------------------------------------------------------------------------
# TAB 2: SUBIR MATERIAL
# ------------------------------------------------------------------------------
with tab_subir:
    st.subheader("Formulario de Aporte Académico")
    with st.form("form_subir", clear_on_submit=True):
        col_carrera, col_ano, col_sem = st.columns(3)
        with col_carrera:
            form_carrera = st.selectbox("Carrera de destino", CARRERAS, index=CARRERAS.index(carrera_sel))
        with col_ano:
            form_ano = st.selectbox("Año", ANOS, index=ANOS.index(ano_sel))
        with col_sem:
            form_semestre = st.selectbox("Semestre", SEMESTRES, index=SEMESTRES.index(semestre_sel))

        form_asig = st.text_input("Nombre de la Asignatura (Ej: Teoría Sociológica I)").strip()
        form_titulo = st.text_input("Título del Material (Ej: Resumen Control 1)").strip()
        form_tipo = st.selectbox("Tipo de Documento", ["Resumen", "Guía de Ejercicios", "Prueba/Pauta Anterior", "Apunte de Clase", "Otro"])
        form_autor = st.text_input("Tu Nombre o Apodo (Opcional)", value="Anónimo").strip()
        form_link = st.text_input("Enlace al archivo (Opcional)").strip()
        form_desc = st.text_area("Descripción breve").strip()
        
        if st.form_submit_button("🚀 Publicar Material"):
            if form_asig and form_titulo and form_link:
                nuevo = {
                    "titulo": form_titulo,
                    "autor": form_autor if form_autor else "Anónimo",
                    "tipo": form_tipo,
                    "link": form_link,
                    "descripcion": form_desc,
                    "votos": 0
                }
                agregar_material(st.session_state.db, form_carrera, form_ano, form_semestre, form_asig, nuevo)
                st.success(f"¡Material '{form_titulo}' publicado con éxito!")
                st.rerun()
            else:
                st.error("Por favor completa los campos obligatorios: Asignatura, Título y Enlace.")