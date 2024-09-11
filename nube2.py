import PyPDF2
import requests
import io
from flask import Flask, jsonify, request  # Esto es para un entorno Flask
app = Flask(__name__)

@app.route('/procesar_pdf', methods=['POST'])
def procesar_pdf():
    data = request.json  # Esto sería en un entorno Flask que recibe solicitudes HTTP
    url_pdf = data.get('https://mailutecedusv-my.sharepoint.com/:f:/g/personal/2514512019_mail_utec_edu_sv/Ev-ZOFI-EspKp4rxjq-cUFQBvyjgPKurTT_A4WvwFeLAdw?e=fN8bh8', '')  # Cambié la clave del JSON a 'url_pdf' por claridad

    if not url_pdf:
        return jsonify({'error': 'URL del PDF no proporcionada'}), 400

    try:
        # Descargar el archivo PDF
        respuesta = requests.get(url_pdf)
        respuesta.raise_for_status()  # Esto asegurará que se maneje un error de descarga

        archivo_pdf = respuesta.content

        # Leer el archivo PDF con PyPDF2
        lector_pdf = PyPDF2.PdfReader(io.BytesIO(archivo_pdf))
        texto = ''
        for pagina in range(len(lector_pdf.pages)):
            texto += lector_pdf.pages[pagina].extract_text()

        # Devolver el texto extraído
        return jsonify({'texto': texto})
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500
    

# Asegúrate de estar ejecutando esto dentro de una aplicación Flask
if __name__ == '__main__':
    app.run(debug=True)