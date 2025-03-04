from flask import Flask, jsonify
from flask_cors import CORS
from app.database import neo4j_conn
from app.routes import nodes, relationships, queries, upload

# Inicializar Flask
app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Registrar Blueprints (rutas)
app.register_blueprint(nodes.bp, url_prefix="/nodes")
#app.register_blueprint(relationships.bp, url_prefix="/relations")
#app.register_blueprint(queries.bp, url_prefix="/queries")
#app.register_blueprint(upload.bp, url_prefix="/upload")

# Ruta de prueba
@app.route("/")
def home():
    return jsonify({"message": "Backend de Neo4j con Flask está corriendo 🚀"})

# Ejecutar el servidor
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
