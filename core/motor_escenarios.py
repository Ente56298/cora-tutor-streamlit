def generar_escenarios(intencion):
    escenario = {
        "id": "escenario_001",
        "nombre": "Reutilizar recursos disponibles",
        "objetivo": intencion.get("objetivo"),
        "recursos_considerados": intencion.get(
            "recursos_disponibles", []
        ),
        "restricciones_a_verificar": intencion.get(
            "restricciones", []
        ),
        "estado": "candidato"
    }

    return [escenario]
