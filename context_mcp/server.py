import requests
from datetime import datetime
import os
import json

class N8nMCPClient:
    """Client per inviare eventi a n8n tramite MCP Protocol (JSON-RPC 2.0)"""
    
    def __init__(self):
        # ⚠️ Nota: Questo URL punta all'interno del network Docker a n8n.
        # Il valore è preso dalla variabile d'ambiente o usa un fallback interno.
        self.webhook_url = os.getenv(
            'N8N_WEBHOOK_URL',
            'http://automazioni_municipio:5678/mcp/6bb9663f-cc05-437f-a027-ab065a4cc1c5'
        )
        
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json, text/event-stream'
        }
        
        self._request_id = 0
    
    def _get_next_id(self):
        """Genera ID incrementale per le richieste JSON-RPC"""
        self._request_id += 1
        return self._request_id
    
    def send_event(self, event_type: str, data: dict, tool_name: str = "notify_event"):
        """
        Invia un evento a n8n tramite JSON-RPC 2.0 (struttura semplificata per webhook).
        
        Args:
            event_type: Tipo di evento (es: 'sensor_reading', 'alert')
            data: Dati dell'evento (dict)
            tool_name: Nome del tool/azione (default: 'notify_event')
        """
        
        # 🛠️ FIX 400 Bad Request: Semplificazione del payload.
        # Spesso i webhook n8n non gestiscono la struttura 'tools/call' complessa
        # e si aspetta i dati rilevanti direttamente nel campo 'params'.
        params_data = {
            "event_type": event_type,
            "timestamp": datetime.now().isoformat(),
            "source": "mcp_server",
            "tool_name": tool_name, 
            "data": data
        }
        
        payload = {
            "jsonrpc": "2.0",
            "id": self._get_next_id(),
            "method": "notify_event", # Usiamo 'notify_event' come nome del metodo
            "params": params_data      # I dati rilevanti sono ora direttamente in 'params'
        }
        
        try:
            response = requests.post(
                self.webhook_url,
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            # Utilizza response.raise_for_status() per catturare 4xx/5xx
            response.raise_for_status() 
            
            # Gestisce il caso di risposta vuota
            result = response.json() if response.text else {}
            
            return {
                "status": "success",
                "code": response.status_code,
                "response": result
            }
            
        except requests.exceptions.HTTPError as e:
            # Cattura errori 4xx o 5xx
            error_detail = e.response.text if e.response else str(e)
            return {
                "status": "error",
                "code": e.response.status_code if e.response else None,
                "message": f"HTTP Error: {error_detail}"
            }
        except requests.exceptions.RequestException as e:
            # Cattura tutti gli altri errori (es. timeout, DNS, connessione)
            return {
                "status": "error",
                "code": None,
                "message": f"Request Error: {str(e)}"
            }
    
    def send_sensor_reading(self, edificio: str, sensore: str, valore: float, unita: str):
        """Helper per inviare letture sensori"""
        return self.send_event(
            event_type="sensor_reading",
            data={
                "edificio": edificio,
                "sensore": sensore,
                "valore": valore,
                "unita": unita
            }
        )
    
    def send_alert(self, edificio: str, tipo_alert: str, messaggio: str, severita: str = "medium"):
        """Helper per inviare alert"""
        return self.send_event(
            event_type="alert",
            data={
                "edificio": edificio,
                "tipo": tipo_alert,
                "messaggio": messaggio,
                "severita": severita
            }
        )


# ============= TEST =============
if __name__ == "__main__":
    client = N8nMCPClient()
    
    # Test 1: Lettura sensore
    print("\n📊 Test 1: Invio lettura sensore...")
    result1 = client.send_sensor_reading(
        edificio="Municipio",
        sensore="temperatura_sala_consiliare",
        valore=23.5,
        unita="°C"
    )
    print(f"Risultato: {json.dumps(result1, indent=2)}")
    
    # Test 2: Alert
    print("\n🚨 Test 2: Invio alert...")
    result2 = client.send_alert(
        edificio="Scuola Elementare",
        tipo_alert="temperature_high",
        messaggio="Temperatura superiore alla soglia critica",
        severita="high"
    )
    print(f"Risultato: {json.dumps(result2, indent=2)}")