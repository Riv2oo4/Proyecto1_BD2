import pandas as pd
from flask import Blueprint, request, jsonify
from app.database import neo4j_conn
import os
from werkzeug.utils import secure_filename

bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Cargar datos desde un archivo CSV
@bp.route("/csv", methods=["POST"])
def upload_csv():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(file_path)
    
    try:
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            query = (
                "CREATE (m:Movie {title: $title, language: $language, popularity: $popularity})"
            )
            params = {
                "title": row["original_title"],
                "language": row["original_language"],
                "popularity": row["popularity"]
            }
            neo4j_conn.run_query(query, params)
        
        return jsonify({"message": "CSV uploaded and processed successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
