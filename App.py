from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import joblib
import os
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer

app = Flask(__name__)




# Load the model and column transformer
model = joblib.load(open("Notebook/best_model.pkl", "rb"))

preprocessor = joblib.load("Notebook/column_transformer.pkl")


def preprocess_data(df):
    processed_data = preprocessor.transform(df) # Transforming the Data 
    return processed_data






 
    
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html') 


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect input data from form
        data = {
    "device_brand": request.form.get("device_brand", "").strip(),
    "os": request.form.get("os", "").strip(),
    "screen_size": float(request.form.get("screen_size", 0) or 0),  # Default 0 if missing
    "4g": int(request.form.get("is_4g", "No") == "Yes"),  # Convert to 0 or 1
    "5g": int(request.form.get("is_5g", "No") == "Yes"),  # Convert to 0 or 1
    "rear_camera_mp": float(request.form.get("rear_camera_mp", 0) or 0),
    "front_camera_mp": float(request.form.get("front_camera_mp", 0) or 0),
    "internal_memory": int(request.form.get("internal_memory", 0) or 0),
    "ram": int(request.form.get("ram", 0) or 0),
    "battery": int(request.form.get("battery", 0) or 0),
    "weight": int(request.form.get("weight", 0) or 0),
    "release_year": int(request.form.get("release_year", 0) or 0),
    "days_used": int(request.form.get("days_used", 0) or 0)
}


        # Save raw data
        raw_df = pd.DataFrame([data])
        raw_df.to_csv('raw_data.csv', mode='a', header=not pd.io.common.file_exists('raw_data.csv'), index=False)

        # Preprocess the data
        processed_data = preprocess_data(raw_df)

        # Prediction (assuming model is already loaded)
        prediction = model.predict(processed_data)

        return f'Predicted Price: {prediction[0]}'

    except Exception as e:
        return str(e)





if __name__ == '__main__':
    app.run(debug=True)
