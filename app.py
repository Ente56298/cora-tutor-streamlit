import streamlit as st

st.set_page_config(
    page_title="CO•RA Tutor",
    page_icon="🧭",
    layout="wide"
)

st.title("🧭 CO•RA Tutor")
st.subheader("Evaluación adaptativa de habilidades")

st.write(
    "Este prototipo evalúa conocimientos, registra evidencia "
    "y recomienda el siguiente paso de aprendizaje."
)

st.divider()

nombre = st.text_input("¿Cómo quieres que te llame el tutor?")

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

respuesta = st.text_area(
    "Diagnóstico inicial",
    placeholder="Escribe qué sabes de esta área o responde la actividad que indique el tutor."
)

if st.button("Evaluar"):
    if not respuesta.strip():
        st.warning("Escribe una respuesta antes de evaluar.")
    else:
        st.success("Respuesta registrada.")

        st.metric("Estado actual", "En exploración")

        st.info(
            f"Área seleccionada: {area}. "
            "En la siguiente versión analizaremos esta respuesta "
            "y generaremos una recomendación personalizada."
        )
