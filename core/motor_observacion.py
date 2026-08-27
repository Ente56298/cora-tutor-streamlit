def crear_observacion_reportada(texto):
    return {
        "origen": "usuario",
        "tipo": "observacion_reportada",
        "texto_original": texto.strip(),
        "interpretacion": None,
        "estado": "sin_verificar"
    }
