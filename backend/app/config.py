import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración de conexión a Neo4j
NEO4J_URI = os.getenv("NEO4J_URI", "neo4j+s://82bfff13.databases.neo4j.io")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "UWNeGWrYs_UYFO_24dOPHgv-SGQomV9wHOQdsWOyh10")