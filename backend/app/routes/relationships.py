from flask import Blueprint, request, jsonify
from app.database import neo4j_conn

bp = Blueprint("relationships", __name__)

@bp.route("/", methods=["POST"])
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

@bp.route("/<label>/<id>", methods=["GET"])
def get_relationships(label, id):
    query = f"MATCH (n:{label})-[r]->(m) WHERE ID(n) = $id RETURN type(r) AS relationship, m"
    result = neo4j_conn.run_query(query, {"id": int(id)})
    
    return jsonify([{ "relationship": record["relationship"], "node": dict(record["m"]) } for record in result])

@bp.route("/<label1>/<id1>/<relationship>/<label2>/<id2>", methods=["DELETE"])
def delete_relationship(label1, id1, relationship, label2, id2):
    query = (
        f"MATCH (a:{label1})-[r:{relationship}]->(b:{label2}) "
        f"WHERE ID(a) = $id1 AND ID(b) = $id2 "
        f"DELETE r"
    )
    neo4j_conn.run_query(query, {"id1": int(id1), "id2": int(id2)})
    
    return jsonify({"message": "Relationship deleted"})