
import gradio as gr

# Symptoms and Diseases Mapping
disease_data = {
    "Influenza (Flu)": ["fever", "cough", "fatigue", "body aches"],
    "COVID-19": ["fever", "cough", "loss of taste", "difficulty breathing"],
    "Common Cold": ["sore throat", "runny nose", "cough", "mild fever"],
}

# Follow-up Questions
follow_up_questions = {
    "fever": "How high is your fever?",
    "cough": "Is your cough dry or with mucus?",
    "fatigue": "Since when are you feeling fatigued?",
}

# Prediction Function
def predict(symptoms):
    symptoms = symptoms.lower().split(",")
    matched_diseases = {}

    for disease, disease_symptoms in disease_data.items():
        matches = len(set(symptoms) & set(disease_symptoms))
        matched_diseases[disease] = matches

    sorted_diseases = sorted(matched_diseases.items(), key=lambda x: x[1], reverse=True)
    top_diseases = [d[0] for d in sorted_diseases if d[1] > 0]

    if not top_diseases:
        return "I'm sorry, I couldn't match your symptoms to any common conditions. Please consult a healthcare provider."

    response = "Based on your symptoms, possible conditions include:\n\n"
    for disease in top_diseases:
        response += f"- {disease}\n"

    follow_ups = []
    for symptom in symptoms:
        symptom = symptom.strip()
        if symptom in follow_up_questions:
            follow_ups.append(follow_up_questions[symptom])

    if follow_ups:
        response += "\nFollow-up Questions:\n"
        for q in follow_ups:
            response += f"- {q}\n"

    response += "\n\nDisclaimer: This tool is for informational purposes only and does not replace professional medical advice. Please consult a doctor if symptoms persist or worsen."
    return response

# Gradio Interface
iface = gr.Interface(
    fn=predict,
    inputs=gr.Textbox(placeholder="Enter your symptoms separated by commas..."),
    outputs="text",
    title="Healthcare AI Assistant",
    description="Enter your symptoms (e.g., fever, cough, fatigue) to get possible health condition suggestions. Built with AI.",
)

iface.launch()
