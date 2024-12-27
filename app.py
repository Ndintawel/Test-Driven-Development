from flask import Flask, render_template, request, jsonify
import spacy
from flask_cors import CORS
from ner_client import NamedEntityClient

app = Flask(__name__)
CORS(app)  # Enable CORS globally

ner = spacy.load("en_core_web_sm")
ner = NamedEntityClient(ner)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ner', methods=['POST'])
def get_named_ents():
    data = request.get_json()
    result = ner.get_ents(data['sentence'])
    return jsonify({"entities": result['ents'], "html": result['html']})

if __name__ == "__main__":
    app.run(debug=True)
