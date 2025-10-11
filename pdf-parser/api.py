from flask import Flask, request, jsonify
import pdfplumber
import io
import re

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'}), 200

@app.route('/parse', methods=['POST'])
def parse_pdf():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Nessun file caricato'}), 400
        
        file = request.files['file']
        pdf_bytes = io.BytesIO(file.read())
        
        sezioni = []
        testo_completo = []
        
        with pdfplumber.open(pdf_bytes) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    testo_completo.append(text)
        
        if not testo_completo:
            return jsonify({'error': 'PDF senza testo estraibile'}), 400
        
        tutto = '\n'.join(testo_completo)
        righe = tutto.split('\n')
        
        sezione_corrente = None
        buffer = []
        
        for riga in righe:
            pulita = riga.strip()
            
            if pulita and len(pulita) >= 5 and len(pulita) <= 60:
                if re.match(r'^[A-Z\s\'\-]+$', pulita) and pulita.count(' ') <= 8:
                    if sezione_corrente and len(buffer) > 3:
                        contenuto = '\n'.join(buffer).strip()
                        if len(contenuto) > 100:
                            sezioni.append({
                                'titolo': sezione_corrente,
                                'testo': contenuto[:2800],
                                'fonte': file.filename,
                                'tipo': 'procedura_comunale'
                            })
                    
                    sezione_corrente = pulita
                    buffer = []
                    continue
            
            if sezione_corrente and pulita:
                buffer.append(pulita)
        
        if sezione_corrente and len(buffer) > 3:
            contenuto = '\n'.join(buffer).strip()
            if len(contenuto) > 100:
                sezioni.append({
                    'titolo': sezione_corrente,
                    'testo': contenuto[:2800],
                    'fonte': file.filename,
                    'tipo': 'procedura_comunale'
                })
        
        if len(sezioni) < 2:
            paragrafi = tutto.split('\n\n')
            sezioni = []
            for i, par in enumerate(paragrafi):
                par = par.strip()
                if len(par) > 200:
                    sezioni.append({
                        'titolo': f'Sezione {i + 1}',
                        'testo': par[:2800],
                        'fonte': file.filename,
                        'tipo': 'procedura_comunale'
                    })
                    if len(sezioni) >= 30:
                        break
        
        return jsonify({
            'status': 'success',
            'sezioni': sezioni,
            'totale': len(sezioni)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)