from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (from frontend)

# Symptom-disease mapping
disease_data = {
    "Influenza (Flu)": ["fever", "cough", "fatigue", "body aches"],
    "COVID-19": ["fever", "cough", "loss of taste", "difficulty breathing"],
    "Common Cold": ["sore throat", "runny nose", "cough", "mild fever"],
}

follow_up_questions = {
    "fever": "How high is your fever?",
    "cough": "Is your cough dry or with mucus?",
    "fatigue": "Since when are you feeling fatigued?",
}

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    symptoms = data.get("symptoms", "").lower().split(",")
    matched = {}

    for disease, sym_list in disease_data.items():
        matched[disease] = len(set(symptoms) & set(sym_list))

    sorted_diseases = sorted(matched.items(), key=lambda x: x[1], reverse=True)
    top = [d[0] for d in sorted_diseases if d[1] > 0]

    if not top:
        return jsonify({"result": "No match. Please consult a doctor."})

    result = f"Possible conditions:\n" + "".join(f"- {d}\n" for d in top)

    followups = [follow_up_questions[s] for s in symptoms if s in follow_up_questions]
    if followups:
        result += "\nFollow-up Questions:\n" + "".join(f"- {q}\n" for q in followups)

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run()

