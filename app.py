import streamlit as st
from backend import (
    CARRERAS,
    ANOS,
    obtener_semestres_por_ano,
    obtener_ramos_oficiales,
    cargar_datos,
    guardar_datos,
    agregar_material,
    agregar_calificacion
)

st.set_page_config(page_title="Proyecto Kula", page_icon="📚", layout="wide")

if "db" not in st.session_state:
    st.session_state.db = cargar_datos()

st.title("📚 Proyecto Kula: Repositorio Académico FACSO")
st.caption("Plataforma de colaboración académica estandarizada según la malla curricular oficial.")

# ------------------------------------------------------------------------------
# FILTROS LATERALES
# ------------------------------------------------------------------------------
st.sidebar.header("👤 Perfil del Estudiante")
carrera_sel = st.sidebar.selectbox("Tu Carrera", CARRERAS)
nivel_estudiante = st.sidebar.selectbox("Tu Nivel Académico Actual", ANOS, index=0)

st.sidebar.divider()
st.sidebar.header("🎯 Navegación de Contenido")
ano_destino = st.sidebar.selectbox("Año a Consultar / Aportar", ANOS, index=ANOS.index(nivel_estudiante))
semestres_disponibles = obtener_semestres_por_ano(ano_destino)
semestre_destino = st.sidebar.selectbox("Semestre", semestres_disponibles)

st.sidebar.divider()
st.sidebar.header("⭐ Filtro de Calidad")
filtro_estrellas = st.sidebar.selectbox(
    "Calificación mínima del apunte",
    ["Todas", "⭐ 4+ Estrellas", "⭐ 3+ Estrellas"]
)

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
            materiales_visibles = 0
            for idx, item in enumerate(materiales):
                titulo = item.get("titulo", "Sin título")
                tipo = item.get("tipo", "Material")
                autor = item.get("autor", "Anónimo")
                desc = item.get("descripcion", "")
                link = item.get("link", "#")
                votos = item.get("votos", 0)
                califs = item.get("calificaciones", [])

                # Cálculo de promedio de completitud/calidad
                promedio = round(sum(califs) / len(califs), 1) if califs else 0.0

                # Aplicar filtro de estrellas
                if filtro_estrellas == "⭐ 4+ Estrellas" and promedio < 4.0 and len(califs) > 0:
                    continue
                if filtro_estrellas == "⭐ 3+ Estrellas" and promedio < 3.0 and len(califs) > 0:
                    continue

                materiales_visibles += 1

                with st.container(border=True):
                    col1, col2 = st.columns([3.5, 1.5])
                    with col1:
                        st.markdown(f"#### 📄 {titulo}")
                        st.markdown(f"**Tipo:** `{tipo}` | **Aportado por:** _{autor}_")
                        if desc:
                            st.write(desc)
                        st.markdown(f"🔗 [Acceder al enlace del archivo]({link})")

                    with col2:
                        # Métrica de Utilidad y Calificación por pares
                        st.metric(label="Utilidad", value=f"👍 {votos}")
                        
                        if califs:
                            st.caption(f"⭐ Calificación: **{promedio} / 5.0** ({len(califs)} eval.)")
                        else:
                            st.caption("⭐ Calificación: _Sin evaluar aún_")

                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            if st.button("👍 Útil", key=f"voto_{asig_sel}_{idx}"):
                                item["votos"] = votos + 1
                                guardar_datos(st.session_state.db)
                                st.rerun()

                        with col_btn2:
                            with st.popover("⭐ Evaluar"):
                                nota = st.slider("Calidad y Completitud", min_value=1, max_value=5, value=5, key=f"slide_{asig_sel}_{idx}")
                                if st.button("Enviar", key=f"rate_{asig_sel}_{idx}"):
                                    agregar_calificacion(
                                        st.session_state.db, 
                                        carrera_sel, 
                                        ano_destino, 
                                        semestre_destino, 
                                        asig_sel, 
                                        idx, 
                                        nota
                                    )
                                    st.success("¡Evaluación enviada!")
                                    st.rerun()

            if materiales_visibles == 0 and len(materiales) > 0:
                st.warning("No hay materiales que cumplan con la calificación mínima seleccionada en la barra lateral.")

# ------------------------------------------------------------------------------
# TAB 2: APORTAR MATERIAL (FRICCIÓN CERO AL SUBIR)
# ------------------------------------------------------------------------------
with tab_subir:
    st.subheader("Formulario de Aporte Académico")

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
                            "votos": 0,
                            "calificaciones": []
                        }
                        agregar_material(st.session_state.db, carrera_sel, ano_destino, semestre_destino, form_asig, nuevo)
                        st.success(f"¡Material '{form_titulo}' publicado con éxito en {form_asig}!")
                        st.rerun()
                    else:
                        st.error("Por favor completa los campos obligatorios: Título y Enlace.")