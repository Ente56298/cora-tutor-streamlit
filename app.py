import streamlit as st

st.set_page_config(
    page_title="CO•RA Tutor",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 CO•RA Tutor")
st.subheader("Evaluación adaptativa de habilidades")

# Identidad mínima
nombre = st.text_input(
    "¿Cómo quieres que te llame?",
    value="•"
)

area = st.selectbox(
    "Selecciona un área para evaluar",
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

    st.write(
        "Con tus propias palabras: "
        "**¿qué es una dirección IP y para qué sirve?**"
    )

    # DIMENSIÓN 1
    st.markdown("#### 1. Comprensión de la consigna")

    interpretacion = st.text_area(
        "Antes de responder, ¿qué entiendes que te está preguntando?",
        placeholder="Explica brevemente qué crees que debes responder."
    )

    # DIMENSIÓN 2
    st.markdown("#### 2. Conocimiento técnico")

    respuesta = st.text_area(
        "Ahora responde la pregunta",
        placeholder="No busques la respuesta. Queremos conocer tu punto de partida."
    )

    if st.button("Evaluar respuesta"):

        if not interpretacion.strip() or not respuesta.strip():
            st.warning(
                "Completa la comprensión de la consigna "
                "y la respuesta técnica."
            )

        else:
            # ==========================================
            # 1. COMPRENSIÓN DE LA CONSIGNA
            # ==========================================

            texto_interpretacion = interpretacion.lower()

            comprension_puntos = 0
            comprension_evidencias = []

            if any(p in texto_interpretacion for p in [
                "qué es",
                "que es",
                "explicar",
                "definir",
                "significa"
            ]):
                comprension_puntos += 1
                comprension_evidencias.append(
                    "Identifica que debe explicar qué es una dirección IP."
                )

            if any(p in texto_interpretacion for p in [
                "para qué sirve",
                "para que sirve",
                "función",
                "funcion",
                "utilidad",
                "sirve"
            ]):
                comprension_puntos += 1
                comprension_evidencias.append(
                    "Identifica que debe explicar para qué sirve una dirección IP."
                )

            if comprension_puntos == 0:
                nivel_comprension = "No clara"
            elif comprension_puntos == 1:
                nivel_comprension = "Parcial"
            else:
                nivel_comprension = "Clara"

            # ==========================================
            # 2. CONOCIMIENTO TÉCNICO
            # ==========================================

            texto = respuesta.lower()

            puntos = 0
            evidencias = []

            # Identificación
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
                    "Reconoce que una IP sirve para identificar "
                    "o direccionar un equipo."
                )

            # Red
            if any(p in texto for p in [
                "red",
                "internet",
                "conectar",
                "conexión",
                "conexion"
            ]):
                puntos += 1
                evidencias.append(
                    "Relaciona la dirección IP con la comunicación en una red."
                )

            # Comunicación / destino
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
                    "Reconoce su función para dirigir comunicaciones "
                    "entre equipos."
                )

            if puntos == 0:
                nivel = "Inicial"
                mensaje = (
                    "Todavía no hay evidencia suficiente "
                    "sobre direccionamiento IP."
                )

            elif puntos == 1:
                nivel = "En exploración"
                mensaje = (
                    "Ya reconoces una parte importante del concepto."
                )

            elif puntos == 2:
                nivel = "En desarrollo"
                mensaje = (
                    "Comprendes los elementos principales "
                    "de una dirección IP."
                )

            else:
                nivel = "Sólido"
                mensaje = (
                    "Tu explicación contiene los conceptos fundamentales."
                )

            # ==========================================
            # RESULTADOS
            # ==========================================

            st.success("Respuesta analizada.")

            st.markdown("### Evaluación por dimensiones")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Comprensión de consigna",
                    f"{comprension_puntos}/2 · {nivel_comprension}"
                )

            with col2:
                st.metric(
                    "Conocimiento técnico",
                    f"{puntos}/3 · {nivel}"
                )

            st.markdown(f"### {nombre} · Redes")

            if comprension_evidencias:
                st.markdown("#### Evidencia de comprensión")

                for evidencia in comprension_evidencias:
                    st.write("•", evidencia)

            if evidencias:
                st.markdown("#### Evidencia técnica")

                for evidencia in evidencias:
                    st.write("•", evidencia)

            st.markdown("#### Interpretación")

            st.write(mensaje)

            st.markdown("#### Siguiente paso")

            if comprension_puntos < 2:
                st.info(
                    "Primero vamos a reforzar la comprensión de la consigna "
                    "antes de aumentar la dificultad técnica."
                )

            elif puntos < 2:
                st.info(
                    "La consigna fue comprendida. Ahora vamos a reforzar "
                    "qué significa identificar un dispositivo dentro de una red."
                )

            else:
                st.info(
                    "La consigna fue comprendida. La siguiente habilidad "
                    "será distinguir IP, gateway y DNS."
                )

else:
    st.info(
        f"El diagnóstico de **{area}** será agregado "
        "después de validar primero el modelo con Redes."
    )
