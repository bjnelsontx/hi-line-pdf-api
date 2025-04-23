import os
import zipfile
import tempfile
from flask import Flask, request, send_file, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_statements():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in request"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.endswith('.zip'):
        return jsonify({"error": "Invalid file format. Only .zip accepted."}), 400

    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, secure_filename(file.filename))
        file.save(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        excel_file = None
        logo_file = None

        for f in os.listdir(tmpdir):
            if f.endswith('.xlsx') or f.endswith('.xls'):
                excel_file = os.path.join(tmpdir, f)
            elif f.lower().endswith(('.png', '.jpg', '.jpeg')):
                logo_file = os.path.join(tmpdir, f)

        if not excel_file or not logo_file:
            missing_debug = f'Files in ZIP: {os.listdir(tmpdir)} | Excel: {excel_file} | Logo: {logo_file}'
            raise Exception(f"Missing file: {missing_debug}")

        # TODO: Replace the line below with actual statement generation logic
        return jsonify({"message": "Successfully received and validated the ZIP file."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
