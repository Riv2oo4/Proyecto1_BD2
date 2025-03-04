from neo4j import GraphDatabase
import sys

# Configuración de conexión
NEO4J_URI = "neo4j+s://82bfff13.databases.neo4j.io"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "UWNeGWrYs_UYFO_24dOPHgv-SGQomV9wHOQdsWOyh10"

# Forzar salida en UTF-8
sys.stdout.reconfigure(encoding='utf-8')

class Neo4jConnector:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def run_query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record for record in result]

# Crear conexión a Neo4j
neo4j_conn = Neo4jConnector(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

# Lista de consultas Cypher
queries = [
    "MATCH (m:Movie) RETURN m.title, m.popularity ORDER BY m.popularity DESC LIMIT 10;",
    "MATCH (m:Movie)-[:BELONGS_TO]->(g:Genre) WHERE g.name = 'Action' RETURN m.title;",
    "MATCH (p:ProductionCompany)<-[:PRODUCED_BY]-(m:Movie) RETURN p.name, COUNT(m) AS total_movies ORDER BY total_movies DESC LIMIT 5;",
    "MATCH (u:User)-[:WATCHED]->(m:Movie) WHERE u.name = 'Alexis' RETURN m.title, m.popularity;",
    "MATCH (u:User)-[:LIKED]->(m:Movie)-[:BELONGS_TO]->(g:Genre)<-[:BELONGS_TO]-(rec:Movie) WHERE u.name = 'Alexis' AND NOT (u)-[:WATCHED]->(rec) RETURN rec.title, COUNT(*) AS relevance ORDER BY relevance DESC LIMIT 5;",
    "MATCH (d:Director)<-[:DIRECTED_BY]-(m:Movie) RETURN d.name, COLLECT(m.title) AS movies_directed;"
]

# Ejecutar cada consulta y mostrar resultados
for i, query in enumerate(queries, start=1):
    print(f"\nEjecutando consulta {i}:")
    results = neo4j_conn.run_query(query)
    for record in results:
        print(str(record).encode('utf-8', 'ignore').decode('utf-8'))

# Cerrar la conexión
neo4j_conn.close()
