from flask import Flask, render_template, request
import os
import joblib
import pandas as pd
import numpy as np

app = Flask(__name__)

# Paths
MODEL_FILE = "model.pkl"
PIPELINE_FILE = "pipeline.pkl"

# Feature names
NUMERIC_FEATURES = ["CreditScore", "Age", "Tenure", "Balance", "NumOfProducts", "HasCrCard", "IsActiveMember", "EstimatedSalary"]
CATEGORICAL_FEATURES = ["Geography", "Gender"]

# Load model and pipeline
def load_model():
    if os.path.exists(MODEL_FILE) and os.path.exists(PIPELINE_FILE):
        model = joblib.load(MODEL_FILE)
        pipeline = joblib.load(PIPELINE_FILE)
        return model, pipeline
    return None, None

model, pipeline = load_model()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or pipeline is None:
        return render_template('index.html', error="Model not found. Please train the model first.")
    
    try:
        # Get form data
        credit_score = float(request.form['CreditScore'])
        age = float(request.form['Age'])
        tenure = float(request.form['Tenure'])
        balance = float(request.form['Balance'])
        num_of_products = float(request.form['NumOfProducts'])
        has_cr_card = int(request.form['HasCrCard'])
        is_active_member = int(request.form['IsActiveMember'])
        estimated_salary = float(request.form['EstimatedSalary'])
        geography = request.form['Geography']
        gender = request.form['Gender']
        
        # Create DataFrame with input data
        input_data = pd.DataFrame({
            'CreditScore': [credit_score],
            'Age': [age],
            'Tenure': [tenure],
            'Balance': [balance],
            'NumOfProducts': [num_of_products],
            'HasCrCard': [has_cr_card],
            'IsActiveMember': [is_active_member],
            'EstimatedSalary': [estimated_salary],
            'Geography': [geography],
            'Gender': [gender]
        })
        
        # Reorder columns to match training data
        input_data = input_data[['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts', 
                                  'HasCrCard', 'IsActiveMember', 'EstimatedSalary', 'Geography', 'Gender']]
        
        # Transform and predict
        transformed_input = pipeline.transform(input_data)
        prediction = model.predict(transformed_input)
        probability = model.predict_proba(transformed_input)[0][1]
        
        result = "Churn (Exited)" if prediction[0] == 1 else "Stay (Not Exited)"
        confidence = round(probability * 100, 2)
        
        return render_template('index.html', 
                             prediction=result, 
                             confidence=confidence,
                             show_result=True)
    
    except Exception as e:
        return render_template('index.html', error=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)
