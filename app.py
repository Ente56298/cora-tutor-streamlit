import json
from datetime import datetime, timezone

import streamlit as st
from ejemplos_fisicos import EJEMPLOS_FISICOS
from core.motor_intencion import crear_intencion
st.set_page_config(
    page_title="CO•RA Tutor",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 CO•RA Tutor")
st.subheader("Trayectoria adaptativa de aprendizaje")
st.caption("Contexto abundante por detrás; simplicidad por delante.")

intencion_texto = st.text_input(
    "¿Qué quieres lograr?"
)

recursos_texto = st.text_input(
    "¿Con qué cuentas ahora?"
)

if intencion_texto.strip():
    intencion = crear_intencion(intencion_texto)
    st.json(intencion)
    
# Memoria temporal del prototipo.
# Por ahora los checkpoints viven durante la sesión de Streamlit.
if "checkpoints" not in st.session_state:
    st.session_state.checkpoints = []

# Identidad mínima
nombre = st.text_input(
    "¿Cómo quieres que te llame?",
    value="•"
)

area = st.selectbox(
    "Selecciona un área para explorar",
    [
        "Redes",
        "Linux",
        "Python",
        "SQL",
        "Web / HTTP",
        "Git y GitHub"
    ]
)

st.divider()

if area == "Redes":

    st.markdown("### Pregunta 1 · Direccionamiento IP")

    pregunta = "¿Qué es una dirección IP y para qué sirve?"
    puente = EJEMPLOS_FISICOS["ip"]
    st.write(
        "Con tus propias palabras: "
        f"**{pregunta}**"
    )

    # ==========================================
    # 1. PUNTO A · CONCEPCIÓN INICIAL
    # ==========================================

    st.markdown("#### 1. Punto A · ¿Qué piensas al respecto?")

    concepcion = st.text_area(
        "Antes de buscar una respuesta correcta, cuéntame cómo lo entiendes tú.",
        placeholder=(
            "Puedes usar ejemplos, comparaciones, recuerdos o dudas. "
            "Aquí no se califica si está bien o mal."
        )
    )

    # ==========================================
    # 2. CONOCIMIENTO DEMOSTRADO
    # ==========================================

    st.markdown("#### 2. ¿Qué puedes explicar con lo que sabes ahora?")

    respuesta = st.text_area(
        "Intenta responder la pregunta",
        placeholder=(
            "No busques información todavía. Queremos registrar "
            "tu punto de partida real."
        )
    )

    if st.button("Crear checkpoint", type="primary"):

        if not concepcion.strip() or not respuesta.strip():
            st.warning(
                "Escribe primero qué piensas y después intenta responder. "
                "Con esas dos piezas podemos construir tu Punto A."
            )

        else:
            texto = f"{concepcion} {respuesta}".lower()
            puntos = 0
            evidencias = []
            brechas = []

            # Evidencia 1 · Identificación / direccionamiento
            if any(p in texto for p in [
                "identifica",
                "identificar",
                "dirección",
                "direccion",
                "dispositivo",
                "equipo"
            ]):
                puntos += 1
                evidencias.append(
                    "Reconoce que una IP puede identificar o direccionar un equipo."
                )
            else:
                brechas.append(
                    "Todavía no aparece con claridad la idea de identificación o direccionamiento."
                )

            # Evidencia 2 · Relación con una red
            if any(p in texto for p in [
                "red",
                "internet",
                "conectar",
                "conexión",
                "conexion"
            ]):
                puntos += 1
                evidencias.append(
                    "Relaciona la dirección IP con equipos conectados en una red."
                )
            else:
                brechas.append(
                    "Todavía no aparece con claridad la relación entre la IP y una red."
                )

            # Evidencia 3 · Comunicación / destino
            if any(p in texto for p in [
                "comunicar",
                "comunicación",
                "comunicacion",
                "enviar",
                "recibir",
                "localizar",
                "destino"
            ]):
                puntos += 1
                evidencias.append(
                    "Reconoce que la IP participa en dirigir comunicaciones entre equipos."
                )
            else:
                brechas.append(
                    "Podemos explorar cómo la dirección IP ayuda a que la información llegue a un destino."
                )

            if puntos == 0:
                nivel = "Exploración inicial"
                interpretacion = (
                    "Aún no hay evidencia suficiente para describir el concepto técnico, "
                    "pero ya tenemos una concepción inicial desde la cual trabajar."
                )
                siguiente_paso = (
                    "Relacionar la idea de dirección con la identificación de un equipo dentro de una red."
                )

            elif puntos == 1:
                nivel = "Primeras conexiones"
                interpretacion = (
                    "Ya aparece una parte importante del concepto. "
                    "Ahora podemos conectarla con las piezas que todavía no aparecen."
                )
                siguiente_paso = (
                    "Conectar identificación, red y comunicación usando un ejemplo sencillo."
                )

            elif puntos == 2:
                nivel = "En desarrollo"
                interpretacion = (
                    "Ya relacionas dos elementos fundamentales del direccionamiento IP."
                )
                siguiente_paso = (
                    "Explorar la pieza que falta y comprobarla con un ejemplo de origen y destino."
                )

            else:
                nivel = "Base sólida"
                interpretacion = (
                    "Tu respuesta contiene las relaciones fundamentales que buscábamos observar."
                )
                siguiente_paso = (
                    "Ahora sigamos por acá: distinguir la función de IP, gateway y DNS en una comunicación."
                )

            checkpoint_id = len(st.session_state.checkpoints) + 1

            checkpoint = {
                "checkpoint": checkpoint_id,
                "version": "0.1",
                "fecha_utc": datetime.now(timezone.utc).isoformat(),
                "persona": nombre.strip() or "•",
                "area": "Redes",
                "tema": "Direccionamiento IP",
                "pregunta": pregunta,
                "punto_a": {
                    "concepcion": concepcion.strip(),
                    "respuesta_actual": respuesta.strip(),
                    "conocimiento_observado": {
                        "puntos": puntos,
                        "maximo": 3,
                        "nivel": nivel
                    }
                },
                "evidencias": evidencias,
                "por_explorar": brechas,
                "puente_fisico": {
                    "concepto": "ip",
                    "ejemplo": puente["ejemplo"],
                    "ayuda": puente["ayuda"],
                    "limite": puente["limite"]
                },
             
                "interpretacion": interpretacion,
                "siguiente_paso": siguiente_paso,
                "fuente": "CO•RA Tutor · interacción directa",
                "estado": "checkpoint_de_sesion"
            }

            st.session_state.checkpoints.append(checkpoint)

            # ==========================================
            # CHECKPOINT V0.1
            # ==========================================

            st.success("Checkpoint creado.")
            st.markdown(f"## 🧭 Checkpoint {checkpoint_id:03d} · Punto A")

            st.markdown("#### Lo que piensas")
            st.write(concepcion)

            st.markdown("#### Lo que ya demostraste")
            if evidencias:
                for evidencia in evidencias:
                    st.write("✓", evidencia)
            else:
                st.write(
                    "Todavía no registramos evidencia técnica suficiente. "
                    "Eso no significa que no exista conocimiento; significa que aún no apareció en esta respuesta."
                )

            st.markdown("#### Lo que podemos explorar")
            if brechas:
                for brecha in brechas:
                    st.write("•", brecha)
            else:
                st.write("• No detectamos una brecha básica en esta primera pregunta.")
                
            st.markdown("#### 🌍 Puente con el mundo físico")
            st.write(f"**Ejemplo:** {puente['ejemplo']}")
            st.write(f"**Ayuda a comprender:** {puente['ayuda']}")
            st.caption(f"Límite de la analogía: {puente['limite']}")
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Evidencia técnica observada",
                    f"{puntos}/3"
                )

            with col2:
                st.metric(
                    "Punto actual",
                    nivel
                )

            st.markdown("#### Interpretación")
            st.write(interpretacion)

            st.markdown("#### Ahora sigamos por acá")
            st.info(siguiente_paso)

            with st.expander("Ver checkpoint como dato estructurado"):
                st.json(checkpoint)

            st.download_button(
                "Descargar checkpoint JSON",
                data=json.dumps(checkpoint, ensure_ascii=False, indent=2),
                file_name=f"cora_checkpoint_{checkpoint_id:03d}.json",
                mime="application/json"
            )

            st.caption(
                "En esta versión los checkpoints se conservan durante la sesión actual. "
                "La persistencia entre sesiones será un paso posterior."
            )

    if st.session_state.checkpoints:
        st.divider()
        st.caption(
            f"Checkpoints creados en esta sesión: {len(st.session_state.checkpoints)}"
        )

else:
    st.info(
        f"La exploración de **{area}** será agregada después de validar "
        "primero el modelo de checkpoints con Redes."
    )
