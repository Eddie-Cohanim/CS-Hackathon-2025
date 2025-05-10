from flask import Flask, request, jsonify
from flask_cors import CORS

from fact_matcher import is_fact_like, check_sentence   # uses new logic

app = Flask(__name__)
CORS(app)

@app.route("/verify_facts", methods=["POST"])
def verify_facts():

    data = request.get_json(force=True) or {}
    print(data)
    results = []

    for sent in data.get("sentences", []):
        if not is_fact_like(sent):
            results.append({"sentence": sent, "label": "skip"})
            continue
        label, sim = check_sentence(sent)
        results.append({"sentence": sent,
                        "label": label,
                        "sim"  : round(sim,3)})
    return jsonify(results=results)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
