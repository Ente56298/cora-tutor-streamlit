"""
CO•RA Tutor — Trayectoria Adaptativa de Aprendizaje
Integración GitHub Memory Bank + Matriz Dorsal de Eventos + Historial ChatGPT
"""
import streamlit as st
import requests
import json
import hashlib
import base64
from datetime import datetime
from pathlib import Path

# ============================================
# CONFIGURACIÓN DE PÁGINA
# ============================================
st.set_page_config(
    page_title="CO•RA Tutor",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CONFIGURACIÓN GITHUB
# ============================================
GITHUB_TOKEN = st.secrets.get("GITHUB_TOKEN", "")
GITHUB_USER = "Ente56298"
REPO_NAME = "CO-RA_Ecosistema_Cognitivo_Inclusivo"

# ============================================
# CLASE PUENTE GITHUB
# ============================================
class CORAGitHubBridge:
    """Puente de integración entre Streamlit y GitHub Memory Bank"""
    
    def __init__(self, token: str, owner: str, repo: str):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def leer_contexto(self, ruta: str):
        """Recupera contexto desde GitHub Memory Bank"""
        url = f"{self.base_url}/{ruta}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            content = base64.b64decode(response.json()["content"]).decode('utf-8')
            return json.loads(content)
        return None
    
    def anclar_evento(self, usuario: str, evento_id: str, payload: dict):
        """Ancla evento en Matriz Dorsal con hash SHA-512"""
        ruta = f"matriz_dorsal/usuarios/{usuario}/eventos.jsonl"
        url = f"{self.base_url}/{ruta}"
        
        response = requests.get(url, headers=self.headers)
        contenido_actual = ""
        sha_actual = ""
        
        if response.status_code == 200:
            contenido_actual = base64.b64decode(response.json()["content"]).decode('utf-8')
            sha_actual = response.json()["sha"]
        
        payload_str = json.dumps(payload, sort_keys=True)
        hash_forense = hashlib.sha512(payload_str.encode('utf-8')).hexdigest()
        
        nuevo_registro = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "evento_id": evento_id,
            "usuario": usuario,
            "hash_sha512": hash_forense,
            "datos": payload
        }
        
        contenido_nuevo = contenido_actual + json.dumps(nuevo_registro) + "\n"
        
        commit_data = {
            "message": f"🔒 [CO•RA] {evento_id} | {usuario}",
            "content": base64.b64encode(contenido_nuevo.encode('utf-8')).decode('utf-8'),
            "branch": "main"
        }
        if sha_actual:
            commit_data["sha"] = sha_actual
        
        return requests.put(url, headers=self.headers, json=commit_data)

# ============================================
# CARGAR CONVERSACIONES EXTRAÍDAS
# ============================================
def cargar_conversaciones():
    """Carga las conversaciones extraídas del archivo JSON"""
    ruta = Path("data/conversaciones_extraidas.json")
    if ruta.exists():
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# ============================================
# INTERFAZ PRINCIPAL
# ============================================
st.title("🧭 CO•RA Tutor")
st.markdown("### Trayectoria adaptativa de aprendizaje")
st.caption("Contexto abundante por detrás; simplicidad por delante.")

# Sidebar - Configuración
with st.sidebar:
    st.header("⚙️ Configuración")
    token = st.text_input("GitHub Token", type="password", value=GITHUB_TOKEN)
    usuario = st.text_input("Usuario", value="Jorge")
    
    if token:
        bridge = CORAGitHubBridge(token, GITHUB_USER, REPO_NAME)
        st.success("✅ Bridge inicializado")

# Tabs principales
tab1, tab2, tab3 = st.tabs([
    " Explorar Área",
    "📚 Historial ChatGPT",
    "🧠 Memory Bank"
])

# ============================================
# TAB 1: EXPLORAR ÁREA
# ============================================
with tab1:
    st.subheader("📋 Contexto Inicial")
    
    col1, col2 = st.columns(2)
    
    with col1:
        objetivo = st.text_input("¿Qué quieres lograr?")
        recursos = st.text_area("¿Con qué cuentas ahora?")
    
    with col2:
        observacion = st.text_area("¿Qué estás observando?")
        nombre = st.text_input("¿Cómo quieres que te llame?", value=usuario)
    
    st.subheader("🎯 Selecciona un área para explorar")
    
    areas = {
        "redes": "🌐 Redes y Direccionamiento IP",
        "programacion": "💻 Programación y Automatización",
        "contable": "📊 Contabilidad y Fiscal (SAT/NIF)",
        "municipal": "️ Gestión Municipal y Transparencia",
        "geoespacial": "🗺️ Sistemas de Información Geográfica",
        "ia": " Inteligencia Artificial y Machine Learning"
    }
    
    area_seleccionada = st.selectbox(
        "Área de conocimiento", 
        list(areas.values()),
        help="Selecciona el área que quieres explorar hoy"
    )
    
    if area_seleccionada:
        st.subheader(f" Pregunta 1 · {area_seleccionada}")
        
        pregunta = "Con tus propias palabras: ¿Qué es una dirección IP y para qué sirve?"
        st.markdown(f"**{pregunta}**")
        
        st.markdown("#### 1. Punto A · ¿Qué piensas al respecto?")
        st.caption("Antes de buscar una respuesta correcta, cuéntame cómo lo entiendes tú.")
        modelo_mental = st.text_area("Tu comprensión actual", height=100)
        
        st.markdown("#### 2. ¿Qué puedes explicar con lo que sabes ahora?")
        st.caption("Intenta responder la pregunta")
        respuesta_ejecucion = st.text_area("Tu respuesta", height=100)
        
        if st.button("🔍 Analizar y Anclar", type="primary"):
            if modelo_mental and respuesta_ejecucion:
                with st.spinner("Procesando a través del núcleo CO•RA..."):
                    if token:
                        bridge.anclar_evento(
                            usuario=nombre,
                            evento_id="TUTOR_MENTAL_MODEL_SUBMITTED",
                            payload={
                                "area": area_seleccionada,
                                "modelo_mental": modelo_mental,
                                "respuesta_ejecucion": respuesta_ejecucion,
                                "objetivo": objetivo,
                                "recursos": recursos,
                                "observacion": observacion
                            }
                        )
                        st.success("✅ Evento anclado en Matriz Dorsal")
                    
                    st.info("🔄 Analizando trayectoria de aprendizaje...")
            else:
                st.warning("⚠️ Por favor completa ambos campos para continuar")

# ============================================
# TAB 2: HISTORIAL CHATGPT
# ============================================
with tab2:
    st.subheader("📚 Historial de Conversaciones ChatGPT")
    st.caption("Contextos previos detectados de tu trayectoria de aprendizaje")
    
    conversaciones = cargar_conversaciones()
    
    if conversaciones:
        # Métricas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Conversaciones", len(conversaciones))
        with col2:
            ancladas = sum(1 for c in conversaciones if c.get('is_pinned'))
            st.metric("Conversaciones Ancladas", ancladas)
        with col3:
            categorias_unicas = len(set(c.get('categoria') for c in conversaciones))
            st.metric("Categorías Exploradas", categorias_unicas)
        
        st.markdown("---")
        
        # Filtros
        col_filtro1, col_filtro2 = st.columns(2)
        with col_filtro1:
            filtro_categoria = st.multiselect(
                "Filtrar por categoría",
                list(set(c.get('categoria') for c in conversaciones)),
                default=[]
            )
        with col_filtro2:
            solo_ancladas = st.checkbox("Mostrar solo ancladas ")
        
        # Aplicar filtros
        conversaciones_filtradas = conversaciones
        if filtro_categoria:
            conversaciones_filtradas = [c for c in conversaciones_filtradas if c.get('categoria') in filtro_categoria]
        if solo_ancladas:
            conversaciones_filtradas = [c for c in conversaciones_filtradas if c.get('is_pinned')]
        
        st.markdown(f"**{len(conversaciones_filtradas)} conversaciones encontradas**")
        
        # Mostrar conversaciones
        for conv in conversaciones_filtradas:
            pinned = "📌" if conv.get('is_pinned') else "💬"
            categoria = conv.get('categoria', 'sin_clasificar')
            
            with st.expander(f"{pinned} {conv.get('titulo')} [{categoria}]"):
                st.write(f"**Categoría:** {categoria}")
                st.write(f"**Anclada:** {'Sí' if conv.get('is_pinned') else 'No'}")
                st.write(f"**Fecha extracción:** {conv.get('fecha_extraccion', 'N/A')}")
                if conv.get('url_completa'):
                    st.link_button("Ver conversación", conv['url_completa'])
    else:
        st.info("No hay conversaciones extraídas. Ejecuta `python extractor_conversaciones.py` primero.")

# ============================================
# TAB 3: MEMORY BANK
# ============================================
with tab3:
    st.subheader("🧠 Memory Bank")
    
    if token and st.button("Cargar contexto desde GitHub"):
        contexto = bridge.leer_contexto(
            f"memory_bank/usuarios/{nombre}/contexto_unificado.json"
        )
        if contexto:
            st.json(contexto)
        else:
            st.info("No hay contexto previo. Este es tu Punto A inicial.")