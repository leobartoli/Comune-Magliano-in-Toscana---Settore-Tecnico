# Usa la tua immagine attuale come base
FROM ankane/pgvector

# Copia TUTTI i file SQL dalla cartella corrente (cioè ./db/)
# Copiamo in una cartella temporanea nel container
COPY *.sql /docker-entrypoint-initdb.d/

# Aggiungiamo il meccanismo di esecuzione forzata:
# Questo script eseguirà l'entrypoint originale di pgvector,
# attenderà l'avvio del DB, ed eseguirà tutti gli script copiati nella cartella di inizializzazione
# (Nota: Eseguiamo gli script DOPO che il server è avviato per aggirare il problema di ankane)

USER postgres

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

# Sostituisci l'entrypoint con il nostro script personalizzato
ENTRYPOINT ["custom-entrypoint.sh"]