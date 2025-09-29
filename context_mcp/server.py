# File: context_mcp/server.py

import os
from flask import Flask

# Inizializza l'applicazione Flask
app = Flask(__name__)

# Recupera le variabili d'ambiente
DATABASE_URL = os.environ.get('DATABASE_URL')
MCP_API_PORT = os.environ.get('PORT', 5000)  # Usa 5000 come fallback se 'PORT' non è definito
# Nota: La variabile d'ambiente PORT è impostata in docker-compose.yml come ${MCP_API_PORT}

@app.route('/')
def home():
    """Endpoint di test per verificare che il server sia attivo."""
    return f"Server Contesto MCP attivo. Connessione DB: {DATABASE_URL}"

@app.route('/context', methods=['GET', 'POST'])
def get_context():
    """Endpoint fittizio per il Model Context Protocol."""
    # Logica per interagire con il DB e Ollama (cervello-analitico) andrebbe qui.
    # Per ora, restituisce un messaggio semplice.
    return {"status": "ok", "message": "Context request received", "db_info": DATABASE_URL}


if __name__ == '__main__':
    # Avvia il server Flask in ascolto su tutte le interfacce (0.0.0.0)
    # e sulla porta specificata dalla variabile d'ambiente PORT (che è ${MCP_API_PORT}).
    print(f"Avvio del Server Contesto MCP sulla porta {MCP_API_PORT}...")
    app.run(host='0.0.0.0', port=int(MCP_API_PORT), debug=True)