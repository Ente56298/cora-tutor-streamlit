"""
CO•RA GitHub Bridge — Puente de Integración Soberana
Conecta contextos aislados y ancla eventos en la Matriz Dorsal
"""
import os
import json
import hashlib
import base64
import requests
from datetime import datetime
from typing import Dict, List, Optional

class CORAGitHubBridge:
    def __init__(self, token: str, owner: str = "Ente56298", 
                 repo: str = "CO-RA_Ecosistema_Cognitivo_Inclusivo"):
        self.token = token
        self.owner = owner
        self.repo = repo
        self.base_url = f"https://api.github.com/repos/{owner}/{repo}/contents"
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
    
    def leer_contexto(self, ruta: str) -> Optional[Dict]:
        url = f"{self.base_url}/{ruta}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            content = base64.b64decode(response.json()["content"]).decode('utf-8')
            return json.loads(content)
        return None
    
    def anclar_evento(self, usuario: str, evento_id: str, payload: Dict):
        ruta = f"matriz_dorsal/usuarios/{usuario}/eventos.jsonl"
        url = f"{self.base_url}/{ruta}"
        
        response = requests.get(url, headers=self.headers)
        contenido_actual = ""
        sha_actual = ""
        
        if response.status_code == 200:
            contenido_actual = base64.b64decode(response.json()["content"]).decode('utf-8')
            sha_actual = response.json()["sha"]
        
        payload_str = json.dumps(payload, sort_keys=True)
        hash_forense = hashlib.sha512(payload_str.encode('utf-8')).hexdigest()
        
        nuevo_registro = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "evento_id": evento_id,
            "usuario": usuario,
            "hash_sha512": hash_forense,
            "datos": payload
        }
        
        contenido_nuevo = contenido_actual + json.dumps(nuevo_registro) + "\n"
        
        commit_data = {
            "message": f"🔒 [CO•RA] {evento_id} | {usuario}",
            "content": base64.b64encode(contenido_nuevo.encode('utf-8')).decode('utf-8'),
            "branch": "main"
        }
        if sha_actual:
            commit_data["sha"] = sha_actual
        
        return requests.put(url, headers=self.headers, json=commit_data)
    
    def guardar_contexto_tutor(self, usuario: str, contexto: Dict):
        ruta = f"memory_bank/usuarios/{usuario}/contexto_unificado.json"
        url = f"{self.base_url}/{ruta}"
        
        sha_actual = ""
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            sha_actual = response.json()["sha"]
            
        commit_data = {
            "message": f"🧠 [CO•RA TUTOR] Contexto unificado para {usuario}",
            "content": base64.b64encode(json.dumps(contexto, indent=2).encode('utf-8')).decode('utf-8'),
            "branch": "main"
        }
        if sha_actual:
            commit_data["sha"] = sha_actual
            
        return requests.put(url, headers=self.headers, json=commit_data).status_code in [200, 201]