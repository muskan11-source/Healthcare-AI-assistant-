
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

    response = f"Based on your symptoms, possible conditions include:\n\n"
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

    response += "\n⚠️ Note: This is for informational purposes only. Consult a doctor for diagnosis."
    return response

# Gradio Blocks Interface
with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as demo:
    gr.Markdown("## 🩺 Healthcare AI Assistant")
    gr.Markdown("_Describe your symptoms and I’ll help you explore possible conditions._")

    with gr.Row():
        input_box = gr.Textbox(placeholder="e.g., fever, cough, fatigue", label="Enter Symptoms")
        submit_btn = gr.Button("Analyze")

    output_box = gr.Textbox(label="Prediction")

    submit_btn.click(predict, inputs=input_box, outputs=output_box)

    gr.Markdown("### ⚠️ _Disclaimer: This is not a diagnosis. Always consult a healthcare provider for serious concerns._")

demo.launch()
