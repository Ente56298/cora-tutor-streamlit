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

# Primera evaluación real
if area == "Redes":

    st.markdown("### Pregunta 1 · Direccionamiento IP")

    st.write(
        "Con tus propias palabras: "
        "**¿qué es una dirección IP y para qué sirve?**"
    )

    st.markdown("#### 1. Comprensión de la consigna")

    interpretacion = st.text_area(
        "Antes de responder, ¿qué entiendes que te está preguntando?",
        placeholder="Explica brevemente qué crees que debes responder."
    )

    st.markdown("#### 2. Conocimiento técnico")

    respuesta = st.text_area(
        "Ahora responde la pregunta",
        placeholder="No busques la respuesta. Queremos conocer tu punto de partida."
    )

    if st.button("Evaluar respuesta"):

        if not respuesta.strip():
            st.warning("Escribe una respuesta antes de evaluar.")

        else:
            texto = respuesta.lower()

            puntos = 0
            evidencias = []

            # Concepto: identificación
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
                    "Reconoce que una IP sirve para identificar o direccionar un equipo."
                )

            # Concepto: red
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

            # Concepto: comunicación/destino
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
                    "Reconoce su función para dirigir comunicaciones entre equipos."
                )

            # Clasificación inicial
            if puntos == 0:
                nivel = "Inicial"
                mensaje = "Todavía no hay evidencia suficiente sobre direccionamiento IP."

            elif puntos == 1:
                nivel = "En exploración"
                mensaje = "Ya reconoces una parte importante del concepto."

            elif puntos == 2:
                nivel = "En desarrollo"
                mensaje = "Comprendes los elementos principales de una dirección IP."

            else:
                nivel = "Sólido"
                mensaje = "Tu explicación contiene los conceptos fundamentales."

            st.success("Respuesta analizada.")

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Estado actual",
                    nivel
                )

            with col2:
                st.metric(
                    "Evidencias detectadas",
                    puntos
                )

            st.markdown(f"### {nombre} · Redes")

            st.write(mensaje)

            if evidencias:
                st.markdown("#### Evidencia")
                for evidencia in evidencias:
                    st.write("•", evidencia)

            st.markdown("#### Siguiente paso")

            if puntos < 2:
                st.info(
                    "Vamos a reforzar qué significa identificar un dispositivo dentro de una red."
                )
            else:
                st.info(
                    "La siguiente habilidad será distinguir IP, gateway y DNS."
                )

else:

    st.info(
        f"El diagnóstico de **{area}** será agregado después de validar primero el modelo con Redes."
    )
