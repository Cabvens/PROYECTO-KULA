import streamlit as st
from backend import (
    CARRERAS,
    ANOS,
    obtener_semestres_por_ano,
    obtener_ramos_oficiales,
    cargar_datos,
    guardar_datos,
    agregar_material
)

st.set_page_config(page_title="Proyecto Kula", page_icon="📚", layout="wide")

if "db" not in st.session_state:
    st.session_state.db = cargar_datos()

st.title("📚 Proyecto Kula: Repositorio Académico FACSO")
st.caption("Plataforma de colaboración académica estandarizada según la malla curricular oficial.")

# Navegación lateral
st.sidebar.header("🎯 Estado Académico")
carrera_sel = st.sidebar.selectbox("Carrera", CARRERAS)
ano_sel = st.sidebar.selectbox("Año Académico", ANOS)

semestres_disponibles = obtener_semestres_por_ano(ano_sel)
semestre_sel = st.sidebar.selectbox("Semestre", semestres_disponibles)

ramos_oficiales = obtener_ramos_oficiales(carrera_sel, ano_sel, semestre_sel)

tab_explorar, tab_subir = st.tabs(["🔍 Explorar Materiales", "📤 Aportar Material"])

# ------------------------------------------------------------------------------
# TAB 1: EXPLORAR MATERIALES
# ------------------------------------------------------------------------------
with tab_explorar:
    st.subheader(f"Navegando: {carrera_sel} > {ano_sel} > {semestre_sel}")

    if not ramos_oficiales:
        st.warning("No hay asignaturas registradas en la malla curricular para este semestre específico.")
    else:
        asig_sel = st.selectbox("Selecciona la Asignatura Oficial:", ramos_oficiales, key="explorar_asig")
        
        carrera_dict = st.session_state.db.get(carrera_sel, {}).get(ano_sel, {}).get(semestre_sel, {})
        materiales = carrera_dict.get(asig_sel, [])

        st.markdown(f"### Materiales para **{asig_sel}** ({len(materiales)})")

        if not materiales:
            st.info(f"💡 Aún no hay archivos subidos para {asig_sel}. ¡Sé el primero en aportar en la pestaña 'Aportar Material'!")
        else:
            for idx, item in enumerate(materiales):
                # Resguardo contra claves faltantes en datos antiguos
                titulo = item.get("titulo", "Sin título")
                tipo = item.get("tipo", "Material")
                autor = item.get("autor", "Anónimo")
                desc = item.get("descripcion", "")
                link = item.get("link", "#")
                votos = item.get("votos", 0)

                with st.container(border=True):
                    col1, col2 = st.columns([4, 1])
                    with col1:
                        st.markdown(f"#### 📄 {titulo}")
                        st.markdown(f"**Tipo:** `{tipo}` | **Aportado por:** _{autor}_")
                        if desc:
                            st.write(desc)
                        st.markdown(f"🔗 [Acceder al enlace del archivo]({link})")

                    with col2:
                        st.metric(label="Utilidad", value=f"👍 {votos}")
                        if st.button("Votar útil", key=f"voto_{asig_sel}_{idx}"):
                            item["votos"] = votos + 1
                            guardar_datos(st.session_state.db)
                            st.rerun()

# ------------------------------------------------------------------------------
# TAB 2: APORTAR MATERIAL
# ------------------------------------------------------------------------------
with tab_subir:
    st.subheader("Formulario de Aporte Académico")
    st.write("Selecciona los datos de tu ramo y comparte tu material con la comunidad.")

    col_c1, col_c2, col_c3 = st.columns(3)
    with col_c1:
        form_carrera = st.selectbox("Carrera de destino", CARRERAS, index=CARRERAS.index(carrera_sel), key="subir_carrera")
    with col_c2:
        form_ano = st.selectbox("Año Académico", ANOS, index=ANOS.index(ano_sel), key="subir_ano")
    with col_c3:
        form_semestres_opciones = obtener_semestres_por_ano(form_ano)
        form_semestre = st.selectbox("Semestre", form_semestres_opciones, key="subir_semestre")

    form_ramos_disponibles = obtener_ramos_oficiales(form_carrera, form_ano, form_semestre)

    if not form_ramos_disponibles:
        st.error("La combinación seleccionada no posee asignaturas en la malla oficial.")
    else:
        form_asig = st.selectbox("Asignatura Oficial de la Malla", form_ramos_disponibles, key="subir_asig")

        with st.form("form_detalles_material", clear_on_submit=True):
            form_titulo = st.text_input("Título del Material (Ej: Resumen Control 1)").strip()
            form_tipo = st.selectbox("Tipo de Documento", ["Resumen", "Guía de Ejercicios", "Prueba/Pauta Anterior", "Apunte de Clase", "Otro"])
            form_autor = st.text_input("Tu Nombre o Apodo (Opcional)", value="Anónimo").strip()
            form_link = st.text_input("Enlace al archivo (Google Drive, Dropbox, etc.)").strip()
            form_desc = st.text_area("Descripción breve del contenido").strip()

            enviado = st.form_submit_button("🚀 Publicar Material")

            if enviado:
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
                    st.success(f"¡Material '{form_titulo}' publicado con éxito para {form_asig} ({form_semestre})!")
                    st.rerun()
                else:
                    st.error("Por favor completa los campos obligatorios: Título y Enlace.")