from flask import Flask, request, jsonify
from src.reasoning_engine.engine import ReasoningEngine

app = Flask(__name__)
reasoning_engine = ReasoningEngine()

@app.route('/reason', methods=['POST'])
def reason():
    data = request.json
    result = reasoning_engine.process(data)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
