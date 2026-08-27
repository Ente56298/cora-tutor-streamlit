"""
Motor de Rastreo de Contextos
Conecta áreas de conocimiento con historial del usuario
"""
from areas_conocimiento import AREAS_CONOCIMIENTO
from typing import List, Dict

class RastreadorContextos:
    def __init__(self):
        self.areas = AREAS_CONOCIMIENTO
    
    def analizar_area_seleccionada(self, area_id: str, historial_usuario: List[Dict]) -> Dict:
        """
        Analiza un área y devuelve:
        1. Contextos previos del usuario relacionados
        2. Áreas conectadas con puentes de conocimiento
        3. Recomendación de inicio basada en su trayectoria
        """
        area = self.areas.get(area_id)
        if not area:
            return {'error': 'Área no encontrada'}
        
        # 1. Rastrear contextos previos
        contextos_previos = area.rastrear_contextos_previos(historial_usuario)
        
        # 2. Identificar áreas conectadas con evidencia
        areas_conectadas_con_evidencia = []
        for area_conectada_id in area.areas_conectadas:
            area_conectada = self.areas.get(area_conectada_id)
            if area_conectada:
                contextos_en_conectada = area_conectada.rastrear_contextos_previos(historial_usuario)
                areas_conectadas_con_evidencia.append({
                    'id': area_conectada_id,
                    'nombre': area_conectada.nombre,
                    'icono': area_conectada.icono,
                    'contextos_encontrados': len(contextos_en_conectada),
                    'es_fortaleza': len(contextos_en_conectada) >= 3
                })
        
        # 3. Generar recomendación de inicio
        recomendacion = self._generar_recomendacion_inicio(area, contextos_previos)
        
        return {
            'area_actual': {
                'id': area.id,
                'nombre': area.nombre,
                'icono': area.icono,
                'descripcion': area.descripcion
            },
            'contextos_previos_detectados': contextos_previos,
            'total_contextos': len(contextos_previos),
            'areas_conectadas': areas_conectadas_con_evidencia,
            'recomendacion_inicio': recomendacion,
            'pregunta_sugerida': area.preguntas_semilla[0] if area.preguntas_semilla else ''
        }
    
    def _generar_recomendacion_inicio(self, area, contextos_previos: List[Dict]) -> str:
        """Genera recomendación personalizada basada en contextos previos"""
        
        if len(contextos_previos) == 0:
            return f"🌱 Esta es tu primera exploración de {area.nombre}. Empezaremos desde los fundamentos."
        
        elif len(contextos_previos) <= 2:
            tema_principal = contextos_previos[0]['titulo']
            return f"🌱 Ya exploraste '{tema_principal}'. Podemos construir sobre esa base."
        
        elif len(contextos_previos) <= 5:
            return f"📚 Tienes {len(contextos_previos)} conversaciones previas en esta área. Nivel intermedio detectado."
        
        else:
            return f"🎯 Eres usuario avanzado en {area.nombre} ({len(contextos_previos)} contextos). Podemos ir directo a casos complejos."