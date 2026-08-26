def crear_intencion(texto):
    return {
        "texto_original": texto,
        "objetivo": None,
        "restricciones": [],
        "recursos_necesarios": [],
        "trazas_relacionadas": [],
        "escenarios": [],
        "ruta_elegida": None,
        "siguiente_paso": None
    }
