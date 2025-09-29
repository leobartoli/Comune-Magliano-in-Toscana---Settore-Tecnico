# File: ./context_mcp/Dockerfile

# 1. Immagine Base
FROM python:3.11-slim

# 2. Directory di Lavoro
WORKDIR /app

# 3. Installazione delle Dipendenze
# Copia il file delle dipendenze e installale
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copia il codice (sebbene il volume lo faccia già, è buona pratica)
COPY server.py .

# Il container è pronto per eseguire il comando specificato in docker-compose.yml