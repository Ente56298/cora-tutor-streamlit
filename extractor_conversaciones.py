"""
Extractor de conversaciones desde HTML de ChatGPT Sidebar
Procesa el archivo conversacion.csv y genera JSON estructurado
"""
import re
import json
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict

def extraer_conversaciones(html_content: str) -> List[Dict]:
    """Extrae conversaciones del HTML de la sidebar de ChatGPT"""
    soup = BeautifulSoup(html_content, 'html.parser')
    conversaciones = []
    
    # Buscar todos los items del historial
    items = soup.find_all(['a', 'li'], attrs={'data-testid': re.compile('history-item.*-options')})
    
    for item in items:
        try:
            # Extraer ID de conversación del href
            href = item.get('href', '')
            conv_id_match = re.search(r'/c/([0-9a-f-]{36})', href)
            conversation_id = conv_id_match.group(1) if conv_id_match else None
            
            if not conversation_id:
                continue
            
            # Extraer título del aria-label
            aria_label = item.get('aria-label', '')
            titulo_match = re.search(r'Abrir opciones de conversación para (.+)', aria_label)
            titulo = titulo_match.group(1) if titulo_match else 'Sin título'
            
            # Detectar si está anclada (pin)
            is_pinned = 'Anclar' in aria_label or item.find('use', href=re.compile('#pin-sm')) is not None
            
            # Clasificar tema automáticamente
            categoria = clasificar_tema(titulo)
            
            # Generar hash único
            import hashlib
            payload = f"{conversation_id}:{titulo}:{datetime.now().isoformat()}"
            hash_auditoria = hashlib.sha512(payload.encode()).hexdigest()
            
            conversacion = {
                'conversation_id': conversation_id,
                'titulo': titulo.strip(),
                'is_pinned': is_pinned,
                'categoria': categoria,
                'url_completa': f"https://chatgpt.com/c/{conversation_id}",
                'hash_auditoria': hash_auditoria,
                'fecha_extraccion': datetime.utcnow().isoformat() + 'Z',
                'fuente': 'ChatGPT Sidebar Export'
            }
            
            # Evitar duplicados
            if not any(c['conversation_id'] == conversation_id for c in conversaciones):
                conversaciones.append(conversacion)
                
        except Exception as e:
            print(f"Error procesando item: {e}")
            continue
    
    return conversaciones

def clasificar_tema(titulo: str) -> str:
    """Clasifica automáticamente el tema de la conversación"""
    titulo_lower = titulo.lower()
    
    categorias = {
        'programacion': ['python', 'excel', 'vba', 'código', 'programar', 'script', 'api', 'app'],
        'municipal': ['pdm', 'pai', 'icati', 'tejupilco', 'municipal', 'transparencia', 'saimes'],
        'contable': ['sat', 'nif', 'agrupador', 'cuenta', 'contab', 'activo', 'fiscal'],
        'geoespacial': ['gis', 'qgis', 'shapefile', 'mapa', 'coordenadas', 'kmz'],
        'ia_machine_learning': ['ia', 'inteligencia artificial', 'gpt', 'chatgpt', 'modelo', 'prompt'],
        'desarrollo_web': ['html', 'css', 'javascript', 'web', 'streamlit'],
        'documentacion': ['word', 'documento', 'pdf', 'archivo'],
        'redes': ['ip', 'red', 'dns', 'router', 'protocolo'],
        'otros': []
    }
    
    for categoria, palabras_clave in categorias.items():
        if any(palabra in titulo_lower for palabra in palabras_clave):
            return categoria
    
    return 'sin_clasificar'

def generar_reporte_analisis(conversaciones: List[Dict]) -> Dict:
    """Genera un reporte analítico del historial"""
    analisis = {
        'total_conversaciones': len(conversaciones),
        'conversaciones_ancladas': sum(1 for c in conversaciones if c.get('is_pinned')),
        'por_categoria': {},
        'temas_frecuentes': {},
        'patrones_detectados': [],
        'fecha_analisis': datetime.utcnow().isoformat() + 'Z'
    }
    
    # Contar por categoría
    for conv in conversaciones:
        cat = conv.get('categoria', 'sin_clasificar')
        analisis['por_categoria'][cat] = analisis['por_categoria'].get(cat, 0) + 1
        
        # Contar palabras frecuentes en títulos
        palabras = conv.get('titulo', '').lower().split()
        for palabra in palabras:
            if len(palabra) > 3:
                analisis['temas_frecuentes'][palabra] = analisis['temas_frecuentes'].get(palabra, 0) + 1
    
    # Detectar patrones
    if analisis['conversaciones_ancladas'] > 5:
        analisis['patrones_detectados'].append(
            "Usuario tiende a anclar conversaciones de referencia técnica"
        )
    
    categorias_top = sorted(analisis['por_categoria'].items(), key=lambda x: x[1], reverse=True)
    if categorias_top:
        analisis['patrones_detectados'].append(
            f"Área principal de interés: {categorias_top[0][0]} ({categorias_top[0][1]} conversaciones)"
        )
    
    return analisis

if __name__ == '__main__':
    # Leer archivo HTML
    with open('conversacion.csv', 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extraer conversaciones
    conversaciones = extraer_conversaciones(html_content)
    print(f"✅ Extraídas {len(conversaciones)} conversaciones")
    
    # Guardar JSON
    with open('data/conversaciones_extraidas.json', 'w', encoding='utf-8') as f:
        json.dump(conversaciones, f, indent=2, ensure_ascii=False)
    
    # Generar reporte
    analisis = generar_reporte_analisis(conversaciones)
    with open('data/analisis_historial.json', 'w', encoding='utf-8') as f:
        json.dump(analisis, f, indent=2, ensure_ascii=False)
    
    print(f"📊 Reporte generado: {analisis['total_conversaciones']} conversaciones")
    print(f" Ancladas: {analisis['conversaciones_ancladas']}")
    print(f"🏆 Categoría top: {list(analisis['por_categoria'].items())[0] if analisis['por_categoria'] else 'N/A'}")