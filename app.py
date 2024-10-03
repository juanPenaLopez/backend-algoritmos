from flask import Flask, jsonify
from flask_cors import CORS
CORS(app)

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Flask backend!"})

if __name__ == '__main__':
    app.run(debug=True)