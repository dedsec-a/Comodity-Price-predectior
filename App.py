from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
from joblib import load

app = Flask(__name__)

# Load the model and one-hot encoder
model = pickle.load(open("Notebook\Best_model.pkl", "rb"))
preprocessor= load("Notebook\preprocessor.pkl" , "rb")

def preprocess_data(data):
    df = pd.DataFrame([data])
    df_encoded = pd.DataFrame(preprocessor.transform(df).toarray())
    return df_encoded

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect input data from form
        data = {
            "device_brand": request.form.get("device_brand"),
            "os": request.form.get("os"),
            "screen_size": float(request.form.get("screen_size")),
            "4g": request.form.get("is_4g") == "Yes",
            "5g": request.form.get("is_5g") == "Yes",
            "rear_camera_mp": float(request.form.get("rear_camera_mp")),
            "front_camera_mp": float(request.form.get("front_camera_mp")),
            "internal_memory": int(request.form.get("internal_memory")),
            "ram": int(request.form.get("ram")),
            "battery": int(request.form.get("battery")),
            "weight": int(request.form.get("weight")),
            "release_year": int(request.form.get("release_year")),
            "days_used": int(request.form.get("days_used"))
        }
        
        # Preprocess the input data
        processed_data = preprocess_data(data)
        
        # Predict price
        prediction = model.predict(processed_data)[0]
        
        return jsonify({"predicted_price": prediction})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
