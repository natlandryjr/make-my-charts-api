from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import os
import uuid

# Folder settings
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

# Initialize app
app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/transcribe-audio', methods=['POST'])
def transcribe_audio():
    if 'audioFile' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['audioFile']
    extension = os.path.splitext(file.filename)[1].lower()
    if extension not in ['.mp3', '.wav', '.m4a']:
        return jsonify({'error': 'Unsupported file type'}), 400

    # Save uploaded file
    uid = str(uuid.uuid4())
    filename = f"{uid}{extension}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    # Simulate sheet music PDF generation
    pdf_filename = f"{uid}.pdf"
    pdf_path = os.path.join(app.config['OUTPUT_FOLDER'], pdf_filename)
    with open(pdf_path, 'wb') as f:
        f.write(b"%PDF-1.4\n%Mock Sheet Music PDF\n%%EOF")

    # Return URL to download the file
    return jsonify({
        "download_url": f"/download/{pdf_filename}"
    })

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
