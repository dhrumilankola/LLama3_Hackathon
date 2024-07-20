from flask import Flask, request, jsonify
from rag_chat import ConversationalRAG
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

document_dir = "./docs"
rag = ConversationalRAG(document_dir)

@app.route("/chat", methods=["POST"])

def chat():
    data = request.json
    query = data.get("query", "")
    if not query:
        return jsonify({"error": "No query provided"}), 400
    response = rag.chat(query)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
