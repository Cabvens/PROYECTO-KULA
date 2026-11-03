import os
import streamlit as st
from backend import (
    CARRERAS,
    ANOS,
    obtener_semestres_por_ano,
    obtener_ramos_oficiales,
    cargar_datos,
    guardar_datos,
    agregar_material,
    agregar_calificacion,
    guardar_archivo_local
)

st.set_page_config(
    page_title="Proyecto Kula | FACSO", 
    page_icon="🔮", 
    layout="wide",
    initial_sidebar_state="expanded"
)

if "db" not in st.session_state:
    st.session_state.db = cargar_datos()

if "votos_usuario" not in st.session_state:
    st.session_state.votos_usuario = set()

# ------------------------------------------------------------------------------
# ESTILOS CSS PERSONALIZADOS
# ------------------------------------------------------------------------------
st.markdown("""
    <style>
    .hero-banner {
        background: linear-gradient(135deg, #6C5CE7 0%, #a29bfe 50%, #ff7675 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 20px rgba(108, 92, 231, 0.2);
    }
    .hero-banner h1 {
        color: white !important;
        font-weight: 800;
        margin-bottom: 0.2rem;
    }
    .hero-banner p {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    .badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.82rem;
        font-weight: 700;
        color: white;
        margin-right: 8px;
    }
    .badge-resumen { background-color: #6C5CE7; }
    .badge-pauta { background-color: #FF7675; }
    .badge-guia { background-color: #00B894; }
    .badge-clase { background-color: #0984E3; }
    .badge-codigo { background-color: #D63031; }
    .badge-otro { background-color: #636E72; }
    
    div[data-testid="stVerticalBlockBorderWrapper"] > div {
        border-left: 6px solid #6C5CE7 !important;
        border-radius: 12px !important;
        background-color: #FFFFFF !important;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    div[data-testid="stVerticalBlockBorderWrapper"]:hover > div {
        box-shadow: 0 6px 16px rgba(0,0,0,0.08) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# BANNER SUPERIOR
# ------------------------------------------------------------------------------
st.markdown("""
    <div class="hero-banner">
        <h1>🔮 Proyecto Kula</h1>
        <p>Circulación colaborativa del conocimiento académico en Ciencias Sociales — FACSO</p>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# BARRA LATERAL
# ------------------------------------------------------------------------------
st.sidebar.markdown("### 👤 Perfil Estudiantil")
carrera_sel = st.sidebar.selectbox("Tu Carrera", CARRERAS)
nivel_estudiante = st.sidebar.selectbox("Tu Nivel Académico Actual", ANOS, index=0)

st.sidebar.divider()
st.sidebar.markdown("### 🎯 Navegación")
ano_destino = st.sidebar.selectbox("Año a Consultar / Aportar", ANOS, index=ANOS.index(nivel_estudiante))
semestres_disponibles = obtener_semestres_por_ano(ano_destino)
semestre_destino = st.sidebar.selectbox("Semestre", semestres_disponibles)

st.sidebar.divider()
st.sidebar.markdown("### ⭐ Filtro de Calidad")
filtro_estrellas = st.sidebar.selectbox(
    "Calificación mínima del apunte",
    ["Todas", "⭐ 4+ Estrellas", "⭐ 3+ Estrellas"]
)

ramos_oficiales = obtener_ramos_oficiales(carrera_sel, ano_destino, semestre_destino)

tab_explorar, tab_subir = st.tabs(["🔍 Explorar Materiales", "📤 Aportar Material"])

def obtener_badge_html(tipo):
    clases = {
        "Resumen": "badge-resumen",
        "Prueba/Pauta Anterior": "badge-pauta",
        "Guía de Ejercicios": "badge-guia",
        "Apunte de Clase": "badge-clase",
        "Script / Código (.R, .py, .csv)": "badge-codigo"
    }
    cls = clases.get(tipo, "badge-otro")
    return f'<span class="badge {cls}">{tipo}</span>'

# ------------------------------------------------------------------------------
# TAB 1: EXPLORAR MATERIALES
# ------------------------------------------------------------------------------
with tab_explorar:
    st.markdown(f"#### 📌 Mostrando: **{carrera_sel}** | **{ano_destino}** | **{semestre_destino}**")

    if not ramos_oficiales:
        st.warning("No hay asignaturas registradas en la malla curricular para este semestre específico.")
    else:
        asig_sel = st.selectbox("📚 Selecciona la Asignatura Oficial:", ramos_oficiales, key="explorar_asig")
        
        carrera_dict = st.session_state.db.get(carrera_sel, {}).get(ano_destino, {}).get(semestre_destino, {})
        materiales = carrera_dict.get(asig_sel, [])

        st.markdown(f"### Materiales en **{asig_sel}** ({len(materiales)})")

        if not materiales:
            st.info(f"💡 Aún no hay archivos subidos para {asig_sel}. ¡Sé el primero en aportar!")
        else:
            materiales_visibles = 0
            for idx, item in enumerate(materiales):
                titulo = item.get("titulo", "Sin título")
                tipo = item.get("tipo", "Otro")
                autor = item.get("autor", "Anónimo")
                desc = item.get("descripcion", "")
                link = item.get("link", "")
                archivo_path = item.get("archivo_path", None)
                nombre_archivo = item.get("nombre_archivo", "archivo")
                votos = item.get("votos", 0)
                califs = item.get("calificaciones", [])

                promedio = round(sum(califs) / len(califs), 1) if califs else 0.0

                if filtro_estrellas == "⭐ 4+ Estrellas" and promedio < 4.0 and len(califs) > 0:
                    continue
                if filtro_estrellas == "⭐ 3+ Estrellas" and promedio < 3.0 and len(califs) > 0:
                    continue

                materiales_visibles += 1
                item_id = f"{carrera_sel}_{ano_destino}_{semestre_destino}_{asig_sel}_{idx}"
                ha_votado = item_id in st.session_state.votos_usuario

                with st.container(border=True):
                    col1, col2 = st.columns([3.6, 1.4])
                    with col1:
                        badge_html = obtener_badge_html(tipo)
                        st.markdown(f"### 📄 {titulo}", unsafe_allow_html=True)
                        st.markdown(f"{badge_html} **Aportado por:** _{autor}_", unsafe_allow_html=True)
                        
                        if desc:
                            st.write(desc)
                        
                        # Manejo de descarga directa o enlace externo
                        if archivo_path and os.path.exists(archivo_path):
                            with open(archivo_path, "rb") as file_data:
                                st.download_button(
                                    label=f"📥 Descargar {nombre_archivo}",
                                    data=file_data,
                                    file_name=nombre_archivo,
                                    key=f"dl_{asig_sel}_{idx}"
                                )
                        elif link:
                            st.markdown(f"🔗 [**Acceder al archivo digital (Enlace)**]({link})")

                    with col2:
                        st.metric(label="Reconocimiento", value=f"👍 {votos}")
                        
                        if califs:
                            st.markdown(f"⭐ **{promedio} / 5.0** <small>({len(califs)} eval.)</small>", unsafe_allow_html=True)
                        else:
                            st.caption("⭐ _Sin evaluar aún_")

                        col_btn1, col_btn2 = st.columns(2)
                        with col_btn1:
                            texto_voto = "💚 Útil" if ha_votado else "👍 Útil"
                            if st.button(texto_voto, key=f"voto_{asig_sel}_{idx}"):
                                if ha_votado:
                                    item["votos"] = max(0, votos - 1)
                                    st.session_state.votos_usuario.remove(item_id)
                                else:
                                    item["votos"] = votos + 1
                                    st.session_state.votos_usuario.add(item_id)
                                
                                guardar_datos(st.session_state.db)
                                st.rerun()

                        with col_btn2:
                            with st.popover("⭐ Evaluar"):
                                nota = st.slider("Calidad / Completitud", 1, 5, 5, key=f"slide_{asig_sel}_{idx}")
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
                                    st.success("¡Enviado!")
                                    st.rerun()

            if materiales_visibles == 0 and len(materiales) > 0:
                st.warning("No hay materiales que cumplan con la calificación mínima seleccionada en el filtro lateral.")

# ------------------------------------------------------------------------------
# TAB 2: APORTAR MATERIAL (SOPORTE PARA ARCHIVOS DIRECTOS Y ENLACES)
# ------------------------------------------------------------------------------
with tab_subir:
    st.markdown("### 📤 Formulario de Aporte Académico")

    idx_estudiante = ANOS.index(nivel_estudiante)
    idx_destino = ANOS.index(ano_destino)

    if idx_destino > idx_estudiante:
        st.error(
            f"🔒 **Restricción de Nivel Académico:** Tu nivel actual es **{nivel_estudiante}**. "
            f"No puedes subir material a **{ano_destino}**. "
            f"Solo puedes aportar apuntes para tu año actual o años anteriores."
        )
    else:
        st.success(f"🎯 **Destino del aporte:** {carrera_sel} ➔ {ano_destino} ➔ {semestre_destino}")

        if not ramos_oficiales:
            st.error("La sección seleccionada no posee asignaturas en la malla oficial.")
        else:
            with st.form("form_aporte_simplificado", clear_on_submit=True):
                form_asig = st.selectbox("Asignatura Oficial de la Malla", ramos_oficiales, key="subir_asig")
                form_titulo = st.text_input("Título del Material (Ej: Guía resuelta Estadística R)").strip()
                form_tipo = st.selectbox("Tipo de Documento", [
                    "Resumen", 
                    "Script / Código (.R, .py, .csv)", 
                    "Guía de Ejercicios", 
                    "Prueba/Pauta Anterior", 
                    "Apunte de Clase", 
                    "Otro"
                ])
                
                # Carga de archivos físicos desde el almacenamiento local
                form_archivo = st.file_uploader(
                    "📁 Cargar archivo desde tu dispositivo (.pdf, .r, .py, .csv, .md, .docx, .xlsx, .zip)", 
                    type=["pdf", "r", "py", "csv", "md", "txt", "docx", "xlsx", "zip", "pptx"]
                )
                
                form_link = st.text_input("O pega un Enlace Externo (Google Drive, Dropbox, etc. - Opcional si subiste archivo)").strip()
                form_autor = st.text_input("Tu Nombre o Apodo (Opcional)", value="Anónimo").strip()
                form_desc = st.text_area("Descripción breve del contenido").strip()

                enviado = st.form_submit_button("🚀 Publicar en el Repositorio")

                if enviado:
                    if form_asig and form_titulo and (form_archivo is not None or form_link):
                        ruta_guardada = None
                        nombre_original = None
                        
                        if form_archivo is not None:
                            ruta_guardada = guardar_archivo_local(form_archivo)
                            nombre_original = form_archivo.name

                        nuevo = {
                            "titulo": form_titulo,
                            "autor": form_autor if form_autor else "Anónimo",
                            "tipo": form_tipo,
                            "link": form_link,
                            "archivo_path": ruta_guardada,
                            "nombre_archivo": nombre_original,
                            "descripcion": form_desc,
                            "votos": 0,
                            "calificaciones": []
                        }
                        agregar_material(st.session_state.db, carrera_sel, ano_destino, semestre_destino, form_asig, nuevo)
                        st.success(f"¡Material '{form_titulo}' publicado con éxito en {form_asig}!")
                        st.rerun()
                    else:
                        st.error("Por favor completa los campos obligatorios: Título y adjunta un Archivo o un Enlace.")