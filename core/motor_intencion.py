def crear_intencion(texto):
    return {
        "texto_original": texto,
        "objetivo": texto.strip()[7:] if texto.strip().lower().startswith("quiero ") else texto.strip(),
        "restricciones": [],
        "recursos_necesarios": [],
        "trazas_relacionadas": [],
        "escenarios": [],
        "ruta_elegida": None,
        "siguiente_paso": None
    }
