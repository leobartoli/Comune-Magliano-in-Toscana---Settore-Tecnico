FROM ankane/pgvector

# Copia TUTTI i file .sql nella cartella standard di inizializzazione del DB.
COPY *.sql /docker-entrypoint-initdb.d/

# ⚠️ CORREZIONE QUI: Rimuoviamo USER postgres qui, lo useremo dopo!

# DEFINISCE LO SCRIPT DI ENTRYPOINT CUSTOM (Eseguito come root, dove i permessi funzionano)
# Lo script è un singolo comando RUN per motivi di efficienza nel Dockerfile.
RUN echo '#!/bin/bash' > /usr/local/bin/custom-entrypoint.sh && \
    echo 'if [ "$1" = "postgres" ]; then' >> /usr/local/bin/custom-entrypoint.sh && \
    echo '  /usr/local/bin/docker-entrypoint.sh "$@"' >> /usr/local/bin/custom-entrypoint.sh && \
    echo '  echo "Waiting for PostgreSQL to start..."' >> /usr/local/bin/custom-entrypoint.sh && \
    echo '  until psql -h localhost -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "select 1" > /dev/null 2>&1; do' >> /usr/local/bin/custom-entrypoint.sh && \
    echo '    sleep 1' >> /usr/local/bin/custom-entrypoint.sh && \
    echo '  done' >> /usr/local/bin/custom-entrypoint.sh && \
    echo '  echo "Database is ready. Executing custom init scripts..."' >> /usr/local/bin/custom-entrypoint.sh && \
    echo '  for f in /docker-entrypoint-initdb.d/*.sql; do psql -h localhost -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f "$f"; done' >> /usr/local/bin/custom-entrypoint.sh && \
    echo 'fi' >> /usr/local/bin/custom-entrypoint.sh && \
    chmod +x /usr/local/bin/custom-entrypoint.sh

# ⚠️ AGGIUNTA QUI: Eseguiamo questo SOLO dopo che lo script è stato creato.
# Da questo punto in poi, l'utente per l'esecuzione del container è 'postgres'.
USER postgres 

# Sostituisci l'Entrypoint del container
ENTRYPOINT ["custom-entrypoint.sh"]
CMD ["postgres"]