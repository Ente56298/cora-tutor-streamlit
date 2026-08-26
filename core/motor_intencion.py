def crear_intencion(texto):
    texto_limpio = texto.strip()

    objetivo = (
        texto_limpio[7:]
        if texto_limpio.lower().startswith("quiero ")
        else texto_limpio
    )

    restricciones = []

    posicion_sin = objetivo.lower().find(" sin ")

    if posicion_sin != -1:
        restriccion = objetivo[posicion_sin + 1:].strip().rstrip(".")
        objetivo = objetivo[:posicion_sin].strip()

        restricciones.append(restriccion)

    return {
        "texto_original": texto,
        "objetivo": objetivo,
        "restricciones": restricciones,
        "recursos_disponibles": [],
        "recursos_necesarios": [],
        "trazas_relacionadas": [],
        "escenarios": [],
        "ruta_elegida": None,
        "siguiente_paso": None
    }
