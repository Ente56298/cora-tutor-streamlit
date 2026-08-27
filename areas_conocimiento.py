"""
Sistema de Áreas de Conocimiento Conectadas
Cada área puede rastrear contextos previos del usuario
"""
from dataclasses import dataclass, field
from typing import List, Dict
from datetime import datetime

@dataclass
class AreaConocimiento:
    id: str
    nombre: str
    icono: str
    descripcion: str
    preguntas_semilla: List[str]
    areas_conectadas: List[str] = field(default_factory=list)
    palabras_clave_rastreo: List[str] = field(default_factory=list)
    
    def rastrear_contextos_previos(self, historial_usuario: List[Dict]) -> List[Dict]:
        """Rastrea conversaciones previas relacionadas con esta área"""
        contextos_encontrados = []
        
        for conv in historial_usuario:
            titulo = conv.get('titulo', '').lower()
            
            if any(palabra in titulo for palabra in self.palabras_clave_rastreo):
                contextos_encontrados.append({
                    'titulo': conv.get('titulo'),
                    'relevancia': self._calcular_relevancia(titulo),
                    'is_pinned': conv.get('is_pinned', False),
                    'fecha_rastreo': datetime.utcnow().isoformat() + 'Z'
                })
        
        return sorted(contextos_encontrados, key=lambda x: x['relevancia'], reverse=True)
    
    def _calcular_relevancia(self, titulo: str) -> float:
        """Calcula qué tan relevante es una conversación para esta área"""
        coincidencias = sum(1 for p in self.palabras_clave_rastreo if p in titulo)
        return coincidencias / len(self.palabras_clave_rastreo)


# ============================================
# DEFINICIÓN DE LAS 8 ÁREAS NUCLEARES
# ============================================

AREAS_CONOCIMIENTO = {
    'redes': AreaConocimiento(
        id='redes',
        nombre='Redes y Direccionamiento',
        icono='🌐',
        descripcion='IP, DNS, protocolos, infraestructura de red',
        preguntas_semilla=[
            '¿Qué es una dirección IP y para qué sirve?',
            '¿Cómo se comunican dos dispositivos en una red?',
            '¿Qué diferencia hay entre IP pública y privada?'
        ],
        areas_conectadas=['programacion', 'geoespacial'],
        palabras_clave_rastreo=['ip', 'red', 'dns', 'router', 'protocolo', 'tcp', 'udp']
    ),
    
    'programacion': AreaConocimiento(
        id='programacion',
        nombre='Programación y Automatización',
        icono='💻',
        descripcion='Python, Excel VBA, APIs, scripts, automatización',
        preguntas_semilla=[
            '¿Qué es una API y cómo permite la comunicación entre sistemas?',
            '¿Cómo automatizarías una tarea repetitiva en Excel?',
            '¿Qué es un script y para qué sirve?'
        ],
        areas_conectadas=['redes', 'ia', 'desarrollo_web', 'contable'],
        palabras_clave_rastreo=['python', 'excel', 'vba', 'macro', 'script', 'api', 'código', 'automat']
    ),
    
    'contable': AreaConocimiento(
        id='contable',
        nombre='Contabilidad y Fiscal (SAT/NIF)',
        icono='📊',
        descripcion='Agrupadores SAT, NIF, catálogo de cuentas, fiscal mexicano',
        preguntas_semilla=[
            '¿Qué es un agrupador SAT y cómo se relaciona con las NIF?',
            '¿Cómo se estructura el catálogo de cuentas?',
            '¿Qué diferencia hay entre activo fijo y activo circulante?'
        ],
        areas_conectadas=['programacion', 'documentacion', 'municipal'],
        palabras_clave_rastreo=['sat', 'nif', 'agrupador', 'cuenta', 'activo', 'fiscal', 'contab', 'catálogo']
    ),
    
    'municipal': AreaConocimiento(
        id='municipal',
        nombre='Gestión Municipal y Transparencia',
        icono='🏛️',
        descripcion='PDM, PAE, transparencia, SAIMEX, gobierno municipal',
        preguntas_semilla=[
            '¿Qué es el PDM y cómo se evalúa su cumplimiento?',
            '¿Cómo funciona la Unidad de Transparencia municipal?',
            '¿Qué es el PAE y para qué sirve?'
        ],
        areas_conectadas=['evaluacion', 'contable', 'geoespacial'],
        palabras_clave_rastreo=['pdm', 'pai', 'transparencia', 'saimes', 'municipal', 'tejupilco', 'icati', 'ayuntamiento']
    ),
    
    'geoespacial': AreaConocimiento(
        id='geoespacial',
        nombre='Sistemas de Información Geográfica',
        icono='🗺️',
        descripcion='QGIS, shapefiles, KMZ, cartografía, georreferenciación',
        preguntas_semilla=[
            '¿Qué es un shapefile y para qué se usa en análisis territorial?',
            '¿Cómo se georreferencia un dato en un mapa?',
            '¿Qué diferencia hay entre vector y raster?'
        ],
        areas_conectadas=['municipal', 'redes', 'evaluacion'],
        palabras_clave_rastreo=['qgis', 'shapefile', 'kmz', 'mapa', 'gis', 'coordenadas', 'geoespacial', 'cartografía']
    ),
    
    'ia': AreaConocimiento(
        id='ia',
        nombre='Inteligencia Artificial y Machine Learning',
        icono='🤖',
        descripcion='IA, LLM, automatización inteligente, agentes',
        preguntas_semilla=[
            '¿Cómo aprende un modelo de IA a partir de datos?',
            '¿Qué es un agente de IA autónomo?',
            '¿Cómo se puede usar IA para automatizar tareas municipales?'
        ],
        areas_conectadas=['programacion', 'desarrollo_web', 'documentacion'],
        palabras_clave_rastreo=['ia', 'inteligencia artificial', 'gpt', 'chatgpt', 'modelo', 'prompt', 'agente', 'machine learning']
    ),
    
    'evaluacion': AreaConocimiento(
        id='evaluacion',
        nombre='Evaluación de Programas y Indicadores',
        icono='📈',
        descripcion='PbR, MIR, indicadores, evaluación de desempeño',
        preguntas_semilla=[
            '¿Qué es la Metodología de Marco Lógico (MIR)?',
            '¿Cómo se construye un indicador de desempeño?',
            '¿Qué diferencia hay entre evaluación de proceso y de resultado?'
        ],
        areas_conectadas=['municipal', 'geoespacial', 'contable'],
        palabras_clave_rastreo=['evaluación', 'indicador', 'mir', 'pbr', 'programa', 'meta', 'pae']
    ),
    
    'desarrollo_web': AreaConocimiento(
        id='desarrollo_web',
        nombre='Desarrollo Web y Aplicaciones',
        icono='',
        descripcion='HTML, CSS, JavaScript, Streamlit, aplicaciones interactivas',
        preguntas_semilla=[
            '¿Cómo se estructura una página web básica?',
            '¿Qué es Streamlit y para qué sirve?',
            '¿Cómo conectar una aplicación web con una base de datos?'
        ],
        areas_conectadas=['programacion', 'ia'],
        palabras_clave_rastreo=['html', 'css', 'javascript', 'streamlit', 'web', 'app', 'frontend', 'backend']
    )
}