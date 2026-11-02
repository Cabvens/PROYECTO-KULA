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

# ------------------------------------------------------------------------------
# FILTROS LATERALES: PERFIL Y NAVEGACIÓN
# ------------------------------------------------------------------------------
st.sidebar.header("👤 Perfil del Estudiante")
carrera_sel = st.sidebar.selectbox("Tu Carrera", CARRERAS)
nivel_estudiante = st.sidebar.selectbox("Tu Nivel Académico Actual", ANOS, index=0)

st.sidebar.divider()
st.sidebar.header("🎯 Navegación de Contenido")
ano_destino = st.sidebar.selectbox("Año a Consultar / Aportar", ANOS, index=ANOS.index(nivel_estudiante))
semestres_disponibles = obtener_semestres_por_ano(ano_destino)
semestre_destino = st.sidebar.selectbox("Semestre", semestres_disponibles)

ramos_oficiales = obtener_ramos_oficiales(carrera_sel, ano_destino, semestre_destino)

tab_explorar, tab_subir = st.tabs(["🔍 Explorar Materiales", "📤 Aportar Material"])

# ------------------------------------------------------------------------------
# TAB 1: EXPLORAR MATERIALES
# ------------------------------------------------------------------------------
with tab_explorar:
    st.subheader(f"Navegando: {carrera_sel} > {ano_destino} > {semestre_destino}")

    if not ramos_oficiales:
        st.warning("No hay asignaturas registradas en la malla curricular para este semestre específico.")
    else:
        asig_sel = st.selectbox("Selecciona la Asignatura Oficial:", ramos_oficiales, key="explorar_asig")
        
        carrera_dict = st.session_state.db.get(carrera_sel, {}).get(ano_destino, {}).get(semestre_destino, {})
        materiales = carrera_dict.get(asig_sel, [])

        st.markdown(f"### Materiales para **{asig_sel}** ({len(materiales)})")

        if not materiales:
            st.info(f"💡 Aún no hay archivos subidos para {asig_sel}. ¡Sé el primero en aportar en la pestaña 'Aportar Material'!")
        else:
            for idx, item in enumerate(materiales):
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
# TAB 2: APORTAR MATERIAL (RESTRINGIDO POR NIVEL Y CONTEXTO HEREDADO)
# ------------------------------------------------------------------------------
with tab_subir:
    st.subheader("Formulario de Aporte Académico")

    # Evaluación de permisos según nivel del alumno
    idx_estudiante = ANOS.index(nivel_estudiante)
    idx_destino = ANOS.index(ano_destino)

    if idx_destino > idx_estudiante:
        st.warning(
            f"🔒 **Restricción de Nivel Académico:** Tu nivel actual registrado es **{nivel_estudiante}**. "
            f"No estás habilitado para subir material a **{ano_destino}**. "
            f"Solo puedes aportar apuntes para tu año actual o años anteriores."
        )
    else:
        st.info(f"📌 Publicando material en: **{carrera_sel}** > **{ano_destino}** > **{semestre_destino}**")

        if not ramos_oficiales:
            st.error("La sección seleccionada no posee asignaturas en la malla oficial.")
        else:
            with st.form("form_aporte_simplificado", clear_on_submit=True):
                form_asig = st.selectbox("Asignatura Oficial de la Malla", ramos_oficiales, key="subir_asig")
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
                        agregar_material(st.session_state.db, carrera_sel, ano_destino, semestre_destino, form_asig, nuevo)
                        st.success(f"¡Material '{form_titulo}' publicado con éxito en {form_asig}!")
                        st.rerun()
                    else:
                        st.error("Por favor completa los campos obligatorios: Título y Enlace.")