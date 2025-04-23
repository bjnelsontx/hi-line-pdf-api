
from flask import Flask, request, send_file
import pandas as pd
import io
import os
import zipfile
from zipfile import ZipFile
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib.pagesizes import LETTER
from reportlab.lib import colors
from reportlab.lib.units import inch
from datetime import datetime
from tempfile import TemporaryDirectory

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_statements():
    if 'input_zip' not in request.files:
        return "Missing file: Please upload a zip file containing 'excel' and 'logo' files.", 400

    input_zip = request.files['input_zip']

    with TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "input.zip")
        input_zip.save(zip_path)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)

        excel_file = None
        logo_file = None
        discovered_files = []

        for root, _, files in os.walk(tmpdir):
            for name in files:
                path = os.path.join(root, name)
                discovered_files.append(path)
                if name.lower().endswith('.xlsx') and not name.startswith('._'):
                    excel_file = path
                if name.lower().endswith(('.jpg', '.jpeg', '.png')) and not name.startswith('._'):
                    logo_file = path

        if not excel_file or not logo_file:
            log = "\n".join([
                "FILES FOUND:",
                *discovered_files,
                "",
                f"Excel File: {excel_file}",
                f"Logo File: {logo_file}"
            ])
            return f"Missing file(s) required for PDF generation. DEBUG INFO:\n{log}", 400

        return "✅ Files found. PDF generation would proceed here.", 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
