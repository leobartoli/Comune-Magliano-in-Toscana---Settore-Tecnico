# 🏛️ Piattaforma Smart per la Gestione del Patrimonio Comunale e della Protezione Civile

Questo repository contiene la configurazione Docker Compose per una piattaforma integrata di **monitoraggio, automazione e analisi** dedicata alla gestione intelligente degli asset e delle infrastrutture di un comune (Smart City / Smart Building).

La soluzione è composta da servizi containerizzati per l'AI, l'IoT, i flussi di lavoro, i database e l'accesso remoto sicuro.

## 📦 Architettura della Piattaforma

Il sistema è suddiviso in cinque aree funzionali principali:

### 🧠 1. Intelligenza Artificiale e Interazione

| Servizio | Funzione | Porta Interna |
| :--- | :--- | :--- |
| **cervello-analitico** | Motore AI locale (Ollama) per analisi predittiva e supporto decisionale. | `11434` |
| **interazione-vocale** | Riconoscimento Vocale (Vosk) per interfacce operatore/sportello. | `2700` |
| **sintesi-vocale-avvisi** | Sintesi Vocale (Piper) per avvisi e notifiche automatiche. | `10200` |

### 🏘️ 2. Automazione e Monitoraggio Infrastrutture

| Servizio | Funzione | Porta Esterna |
| :--- | :--- | :--- |
| **piattaforma-iot** | Piattaforma di integrazione (Home Assistant) per sensori, BMS e dispositivi IoT. | `8123` |
| **flussi-manutenzione** | Motore di workflow (n8n) per automatizzare processi, notifiche e manutenzioni. | `5678` |

### 💾 3. Database e Cache Dati

| Servizio | Funzione | Porta Esterna |
| :--- | :--- | :--- |
| **database-patrimonio** | Database PostgreSQL per anagrafica beni e stati. | `5432` |
| **cache-dati** | Redis per cache ad alta velocità e code di messaggi. | `6379` |

### 📊 4. Analisi e Visualizzazione

| Servizio | Funzione | Porta Esterna |
| :--- | :--- | :--- |
| **telemetria-sensori** | Database InfluxDB per serie storiche e telemetria da sensori. | `8086` |
| **dashboard-report** | Dashboard Grafana per reportistica, grafici e monitoraggio in tempo reale. | `3000` |

### 🔒 5. Accesso Sicuro e Reti Esterne

| Servizio | Funzione | Note |
| :--- | :--- | :--- |
| **tunnel-accesso-remoto** | Cloudflare Tunnel per accesso remoto sicuro senza aprire porte. | Dipende da `piattaforma-iot` e `dashboard-report`. |
| **rete-infrastrutture-remote** | ZeroTier VPN per collegare centraline o sedi remote al network principale. | Utilizza `network_mode: host`. |

---

## 🚀 Guida all'Installazione

### 1. Prerequisiti

È necessario avere installati:

* **Docker**
* **Docker Compose (Plugin)**
* (Opzionale) **Driver NVIDIA** e **NVIDIA Container Toolkit** se si vuole utilizzare l'accelerazione GPU per `cervello-analitico`.

### 2. Configurazione

Crea il file di configurazione delle variabili d'ambiente copiando l'esempio fornito:

```bash
cp .env.example .env

### Credenziali n8n:
