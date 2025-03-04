from flask import Blueprint, request, jsonify
from app.database import neo4j_conn
from app.models.movie import Movie

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
    
    count = result.single()["total"] if result.peek() else 0
    return jsonify({"label": label, "count": count})
