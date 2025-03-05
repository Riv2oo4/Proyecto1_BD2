from flask import Blueprint, request, jsonify
from app.database import neo4j_conn
from app.models.movie import Movie
from app.models.users import User

bp = Blueprint("nodes", __name__)

# Crear un nodo
@bp.route("/", methods=["POST"])
def create_node():
    data = request.json
    labels = data.get("labels", [])  # Lista de etiquetas
    properties = data.get("properties", {})

    if not labels or not isinstance(labels, list) or len(labels) < 1:
        return jsonify({"error": "At least one label is required"}), 400

    label_string = ":".join(labels)

    query = f"CREATE (n:{label_string} $props) RETURN n"
    result = neo4j_conn.run_query(query, {"props": properties})

    return jsonify({"message": "Node created", "node": str(result)})


# Obtener todos los nodos de un tipo
@bp.route("/<label>", methods=["GET"])
def get_nodes(label):
    query = f"MATCH (n:{label}) RETURN n LIMIT 50"
    result = neo4j_conn.run_query(query)
    
    nodes = []
    for record in result:
        node_data = dict(record["n"])
        if label == "Movie":
            nodes.append(Movie(**node_data).to_dict())
        elif label == "User":
            nodes.append(User(**node_data).to_dict())
        else:
            nodes.append(node_data)
    
    return jsonify(nodes)

# Obtener un nodo por ID
@bp.route("/<label>/<id>", methods=["GET"])
def get_node(label, id):
    query = f"MATCH (n:{label}) WHERE ID(n) = $id RETURN n"
    result = neo4j_conn.run_query(query, {"id": int(id)})
    
    if result:
        node_data = dict(result[0]["n"])
        if label == "Movie":
            return jsonify(Movie(**node_data).to_dict())
        elif label == "User":
            return jsonify(User(**node_data).to_dict())
        else:
            return jsonify(node_data)
    
    return jsonify({"error": "Node not found"}), 404

# Actualizar un nodo
@bp.route("/<label>/<id>", methods=["PUT"])
def update_node(label, id):
    data = request.json
    updates = ", ".join(f"n.{k} = ${k}" for k in data.keys())
    query = f"MATCH (n:{label}) WHERE ID(n) = $id SET {updates} RETURN n"
    params = {"id": int(id), **data}
    result = neo4j_conn.run_query(query, params)
    
    return jsonify({"message": "Node updated", "node": str(result)}) if result else jsonify({"error": "Node not found"}), 404

# Eliminar un nodo
@bp.route("/<label>/<id>", methods=["DELETE"])
def delete_node(label, id): 
    query = f"MATCH (n:{label}) WHERE ID(n) = $id DETACH DELETE n"
    neo4j_conn.run_query(query, {"id": str(id)})
    
    return jsonify({"message": "Node deleted"})