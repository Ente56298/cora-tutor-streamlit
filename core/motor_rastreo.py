"""
Motor de Rastreo de Contextos
Conecta áreas de conocimiento con historial del usuario
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
        contextos_encontrados = []
        for conv in historial_usuario:
            titulo = conv.get('titulo', '').lower()
            if any(palabra in titulo for palabra in self.palabras_clave_rastreo):
                contextos_encontrados.append({
                    'titulo': conv.get('titulo'),
                    'relevancia': self._calcular_relevancia(titulo),
                    'is_pinned': conv.get('is_pinned', False)
                })
        return sorted(contextos_encontrados, key=lambda x: x['relevancia'], reverse=True)
    
    def _calcular_relevancia(self, titulo: str) -> float:
        coincidencias = sum(1 for p in self.palabras_clave_rastreo if p in titulo)
        return coincidencias / len(self.palabras_clave_rastreo)

AREAS_CONOCIMIENTO = {
    'redes': AreaConocimiento(
        id='redes', nombre='Redes y Direccionamiento', icono='🌐',
        descripcion='IP, DNS, protocolos, infraestructura de red',
        preguntas_semilla=['¿Qué es una dirección IP y para qué sirve?'],
        areas_conectadas=['programacion', 'geoespacial'],
        palabras_clave_rastreo=['ip', 'red', 'dns', 'router', 'protocolo']
    ),
    'programacion': AreaConocimiento(
        id='programacion', nombre='Programación y Automatización', icono='💻',
        descripcion='Python, Excel VBA, APIs, scripts',
        preguntas_semilla=['¿Qué es una API y cómo permite la comunicación entre sistemas?'],
        areas_conectadas=['redes', 'ia', 'contable'],
        palabras_clave_rastreo=['python', 'excel', 'vba', 'script', 'api', 'código']
    ),
    'contable': AreaConocimiento(
        id='contable', nombre='Contabilidad y Fiscal (SAT/NIF)', icono='📊',
        descripcion='Agrupadores SAT, NIF, catálogo de cuentas',
        preguntas_semilla=['¿Qué es un agrupador SAT y cómo se relaciona con las NIF?'],
        areas_conectadas=['programacion', 'municipal'],
        palabras_clave_rastreo=['sat', 'nif', 'agrupador', 'cuenta', 'fiscal', 'contab']
    ),
    'municipal': AreaConocimiento(
        id='municipal', nombre='Gestión Municipal y Transparencia', icono='🏛️',
        descripcion='PDM, PAE, transparencia, SAIMEX',
        preguntas_semilla=['¿Qué es el PDM y cómo se evalúa su cumplimiento?'],
        areas_conectadas=['evaluacion', 'contable', 'geoespacial'],
        palabras_clave_rastreo=['pdm', 'pai', 'transparencia', 'saimes', 'municipal', 'tejupilco']
    ),
    'geoespacial': AreaConocimiento(
        id='geoespacial', nombre='Sistemas de Información Geográfica', icono='🗺️',
        descripcion='QGIS, shapefiles, KMZ, cartografía',
        preguntas_semilla=['¿Qué es un shapefile y para qué se usa?'],
        areas_conectadas=['municipal', 'redes'],
        palabras_clave_rastreo=['qgis', 'shapefile', 'kmz', 'mapa', 'gis', 'coordenadas']
    ),
    'ia': AreaConocimiento(
        id='ia', nombre='Inteligencia Artificial', icono='🤖',
        descripcion='IA, LLM, automatización inteligente',
        preguntas_semilla=['¿Cómo aprende un modelo de IA a partir de datos?'],
        areas_conectadas=['programacion', 'desarrollo_web'],
        palabras_clave_rastreo=['ia', 'inteligencia artificial', 'gpt', 'chatgpt', 'modelo', 'prompt']
    ),
    'evaluacion': AreaConocimiento(
        id='evaluacion', nombre='Evaluación de Programas', icono='📈',
        descripcion='PbR, MIR, indicadores, evaluación',
        preguntas_semilla=['¿Qué es la Metodología de Marco Lógico?'],
        areas_conectadas=['municipal', 'contable'],
        palabras_clave_rastreo=['evaluación', 'indicador', 'mir', 'pbr', 'programa', 'pae']
    ),
    'desarrollo_web': AreaConocimiento(
        id='desarrollo_web', nombre='Desarrollo Web', icono='🌍',
        descripcion='HTML, CSS, JavaScript, Streamlit',
        preguntas_semilla=['¿Cómo se estructura una página web básica?'],
        areas_conectadas=['programacion', 'ia'],
        palabras_clave_rastreo=['html', 'css', 'javascript', 'streamlit', 'web', 'app']
    )
}