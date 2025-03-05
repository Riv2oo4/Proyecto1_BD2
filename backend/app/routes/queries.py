from flask import Blueprint, request, jsonify
from app.database import neo4j_conn
from app.models.movie import Movie
from app.models.users import User

bp = Blueprint("queries", __name__)

# Obtener las películas más populares
@bp.route("/movies/popular", methods=["GET"])
def get_popular_movies():
    query = "MATCH (m:Movie) RETURN m ORDER BY m.popularity DESC LIMIT 10"
    result = neo4j_conn.run_query(query)

    movies = [Movie(**dict(record["m"])).to_dict() for record in result]
    
    return jsonify(movies)

# Obtener películas por género
@bp.route("/movies/genre/<genre>", methods=["GET"])
def get_movies_by_genre(genre):
    query = "MATCH (m:Movie)-[:BELONGS_TO]->(g:Genre) WHERE g.name = $genre RETURN m"
    result = neo4j_conn.run_query(query, {"genre": genre})
    
    movies = [Movie(**dict(record["m"])).to_dict() for record in result]
    return jsonify(movies)

# Obtener recomendaciones personalizadas para un usuario
@bp.route("/recommendations/<user_id>", methods=["GET"])
def get_recommendations(user_id):
    query = (
        "MATCH (u:User)-[:LIKED]->(m:Movie)-[:BELONGS_TO]->(g:Genre)<-[:BELONGS_TO]-(rec:Movie) "
        "WHERE ID(u) = $user_id AND NOT (u)-[:WATCHED]->(rec) "
        "RETURN rec"
    )   
    result = neo4j_conn.run_query(query, {"user_id": int(user_id)})
    
    recommendations = [Movie(**dict(record["rec"])).to_dict() for record in result]
    return jsonify(recommendations)

# Ver todas las películas que un usuario ha visto
@bp.route("/users/<user_id>/watched", methods=["GET"])
def get_watched_movies(user_id):
    query = "MATCH (u:User)-[:WATCHED]->(m:Movie) WHERE ID(u) = $user_id RETURN m"
    result = neo4j_conn.run_query(query, {"user_id": int(user_id)})
    
    watched_movies = [Movie(**dict(record["m"])).to_dict() for record in result]
    return jsonify(watched_movies)

# Obtener nodos con límite
@bp.route("/get_nodos/<int:limit>", methods=["GET"])
def get_nodes(limit):
    query = "MATCH (n) RETURN n LIMIT $limit"
    result = neo4j_conn.run_query(query, {"limit": limit})
    
    nodes = [record["n"]._properties for record in result]  # Acceder a las propiedades del nodo
    return jsonify(nodes)

# Consultar un nodo por una propiedad específica
@bp.route("/nodes/property/<property_name>/<property_value>", methods=["GET"])
def get_node_by_property(property_name, property_value):
    query = f"MATCH (n) WHERE n.{property_name} = $property_value RETURN n LIMIT 1"
    result = neo4j_conn.run_query(query, {"property_value": property_value})
    
    nodes = [record["n"]._properties for record in result]
    return jsonify(nodes)

# Consultar muchos nodos con filtro en una propiedad
@bp.route("/nodes/filter/<property_name>/<property_value>", methods=["GET"])
def get_nodes_by_filter(property_name, property_value):
    query = f"MATCH (n) WHERE n.{property_name} = $property_value RETURN n"
    result = neo4j_conn.run_query(query, {"property_value": property_value})
    
    nodes = [record["n"]._properties for record in result]
    return jsonify(nodes)

# Consulta agregada: Contar la cantidad de nodos de un tipo específico
@bp.route("/nodes/count/<label>", methods=["GET"])
def count_nodes_by_label(label):
    query = f"MATCH (n:{label}) RETURN COUNT(n) AS total"
    result = neo4j_conn.run_query(query)
    
    count = result[0]["total"] if result else 0
    return jsonify({"label": label, "count": count})

# Eliminar múltiples nodos
@bp.route("/nodes/delete/<label>", methods=["DELETE"])
def delete_multiple_nodes(label):
    query = f"MATCH (n:{label}) WITH n LIMIT 30 DETACH DELETE n RETURN COUNT(n) AS deleted"
    result = neo4j_conn.run_query(query)
    count = result[0]["deleted"] if result else 0
    return jsonify({"message": "Nodes deleted", "count": count})

# Crear relación con propiedades
@bp.route("/relationships", methods=["POST"])
def create_relationship():
    data = request.json
    node1_label = data.get("node1_label")
    node1_id = data.get("node1_id")
    node2_label = data.get("node2_label")
    node2_id = data.get("node2_id")
    relationship_type = data.get("relationship_type")
    properties = data.get("properties", {})
    
    if not all([node1_label, node1_id, node2_label, node2_id, relationship_type]):
        return jsonify({"error": "All fields are required"}), 400
    
    query = (
        f"MATCH (a:{node1_label}), (b:{node2_label}) "
        f"WHERE ID(a) = $node1_id AND ID(b) = $node2_id "
        f"CREATE (a)-[r:{relationship_type} $props]->(b) RETURN r"
    )
    result = neo4j_conn.run_query(query, {"node1_id": int(node1_id), "node2_id": int(node2_id), "props": properties})
    
    return jsonify({"message": "Relationship created", "relationship": str(result)})



@bp.route("/users/watched_details", methods=["GET"])
def get_watched_movies_details():
    query = "MATCH p=()-[:WATCHED]->() RETURN p LIMIT 25;"
    result = neo4j_conn.run_query(query)

    # Transformar los datos en una lista de diccionarios JSON
    movies_list = []
    
    for record in result:
        path = record["p"]
        start_node = path.nodes[0]  # Primer nodo (Usuario)
        end_node = path.nodes[-1]   # Último nodo (Película)
        
        user_data = {
            "name": start_node["name"],
            "age": start_node["age"],
            "email": start_node["email"]
        }
        
        movie_data = {
            "title": end_node["title"],
            "popularity": end_node["popularity"],
            "language": end_node["language"]
        }
        
        movies_list.append({
            "user": user_data,
            "movie": movie_data
        })

    return jsonify(movies_list)
