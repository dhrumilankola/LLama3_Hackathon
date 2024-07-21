from flask import Flask, request, jsonify
from flask_cors import CORS
from insurance_rag import InsuranceRAG
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = './uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize InsuranceRAG for each type
insurance_rags = {
    'dental': InsuranceRAG('dental'),
    'vision': InsuranceRAG('vision'),
    'medical': InsuranceRAG('medical'),
    'custom': InsuranceRAG('custom')
}

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    query = data.get("query", "")
    insurance_type = data.get("insurance_type", "").lower()
    print(f"Received request: query={query}, insurance_type={insurance_type}")  # Add this line
    if not query or insurance_type not in insurance_rags:
        return jsonify({"error": f"Invalid query or insurance type. Received: query={query}, insurance_type={insurance_type}"}), 400
    response = insurance_rags[insurance_type].chat(query)
    return jsonify({"response": response})

@app.route("/clear_chat", methods=["POST"])
def clear_chat():
    data = request.json
    insurance_type = data.get("insurance_type", "").lower()
    if insurance_type not in insurance_rags:
        return jsonify({"error": "Invalid insurance type"}), 400
    insurance_rags[insurance_type].clear_history()
    return jsonify({"message": f"Chat history cleared for {insurance_type} insurance"}), 200

@app.route("/upload", methods=["POST"])
def upload_file():
    print("Upload request received")
    if 'file' not in request.files:
        print("No file part in the request")
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        print("No selected file")
        return jsonify({"error": "No selected file"}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        print(f"File saved to {file_path}")
        try:
            insurance_rags['custom'].add_document(file_path)
            print("Document added to custom insurance RAG")
            return jsonify({"message": "File successfully uploaded and processed"}), 200
        except Exception as e:
            print(f"Error processing file: {str(e)}")
            return jsonify({"error": f"Error processing file: {str(e)}"}), 500
    print("Invalid file type")
    return jsonify({"error": "Invalid file type"}), 400

@app.route("/remove_custom_documents", methods=["POST"])
def remove_custom_documents():
    insurance_rags['custom'].remove_all_documents()
    return jsonify({"message": "All custom documents removed"}), 200

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

if __name__ == "__main__":
    app.run(debug=True)