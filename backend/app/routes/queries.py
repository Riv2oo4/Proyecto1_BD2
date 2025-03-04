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