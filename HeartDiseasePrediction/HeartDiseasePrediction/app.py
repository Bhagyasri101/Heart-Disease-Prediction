from flask import Flask, request, jsonify, send_from_directory
import pickle
import numpy as np
import os
import pandas as pd

# Initialize the Flask app
app = Flask(__name__)

# Load the trained model
model = pickle.load(open("model.pkl", "rb"))

# Serve the index.html file
@app.route("/")
def home():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Parse JSON data from the POST request
        data = request.get_json()

        # Ensure all required fields are in the input data
        required_fields = [
            "age", "sex", "cp", "trestbps", "chol", "fbs", 
            "restecg", "thalach", "exang", "oldpeak", 
            "slope", "ca", "thal"
        ]
        
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Create a DataFrame with the correct feature names
        feature_names = required_fields
        features = pd.DataFrame([[float(data[field]) for field in feature_names]], columns=feature_names)

        # Debugging: Print the DataFrame to verify the input format
        print("Input Features DataFrame:", features)

        # Predict using the model
        prediction = model.predict(features)

        # Debugging: Print the prediction output
        print("Model Prediction:", prediction)

        # Prepare personalized recommendations based on prediction
        recommendations = get_recommendations(prediction[0])

        # Debugging: Print the recommendations
        print("Recommendations:", recommendations)

        # Return the prediction result with recommendations
        return jsonify({
            "prediction": int(prediction[0]),
            "recommendations": recommendations
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_recommendations(risk_level):
    """Function to return recommendations based on the risk level"""
    if risk_level == 1:  # High risk of heart disease
        return {
            "risk_level": "High Risk of Heart Disease",
            "diet": [
                "Increase intake of fiber-rich foods (e.g., fruits, vegetables, oats).",
                "Eat healthy fats (e.g., salmon, almonds).",
                "Limit processed foods and sugary snacks.",
            ],
            "exercise": [
                "Engage in regular cardiovascular exercises (e.g., walking, cycling).",
                "Aim for at least 150 minutes of moderate exercise per week.",
            ],
            "lifestyle": [
                "Quit smoking if you are a smoker.",
                "Limit alcohol consumption.",
                "Get regular check-ups to monitor heart health."
            ]
        }
    else:  # Low risk of heart disease
        return {
            "risk_level": "Low Risk of Heart Disease",
            "diet": [
                "Continue eating a balanced diet rich in fruits, vegetables, and whole grains.",
                "Maintain moderate intake of lean proteins and healthy fats.",
            ],
            "exercise": [
                "Keep up with regular physical activity (e.g., walking, yoga).",
                "Aim to exercise at least 150 minutes per week.",
            ],
            "lifestyle": [
                "Continue monitoring your health with regular check-ups.",
                "Maintain a healthy weight and stay active."
            ]
        }

if __name__ == "__main__":
    app.run(debug=True)
