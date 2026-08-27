# Motor de evaluación de escenarios de CO•RA
def evaluar_escenario(escenario):
    restricciones_pendientes = escenario.get(
        "restricciones_a_verificar", []
    )

    evaluacion = {
        "escenario_id": escenario.get("id"),
        "objetivo_definido": bool(
            escenario.get("objetivo")
        ),
        "recursos_presentes": bool(
            escenario.get("recursos_considerados")
        ),
        "restricciones_pendientes": restricciones_pendientes,
        "estado": (
            "requiere_verificacion"
            if restricciones_pendientes
            else "sin_restricciones_pendientes"
        )
    }

    return evaluacion
