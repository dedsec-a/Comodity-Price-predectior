from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Loading the Model and Preprocessor
model = joblib.load("Notebook/Best_model.pkl")
cat_features = joblib.load("Notebook/Catagorical_features.pkl")
num_features = joblib.load("Notebook/Numerical_Features.pkl")
preprocessor = joblib.load("Notebook/Preprocessor.pkl")

def preprocess_data(df):
    df_nums = df[num_features]
    df_cat = df[cat_features]
    combined_data = pd.concat([df_nums, df_cat], axis=1)
    return preprocessor.transform(combined_data)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET','POST'])
def predict():
    try:
     if request.method == 'POST':
        data = {
            "device_brand": request.form.get("device_brand", "").strip(),
            "os": request.form.get("os", "").strip(),
            "screen_size": float(request.form.get("screen_size", 0) or 0),
            "4g": int(request.form.get("is_4g", "No").lower() == "yes"),
            "5g": int(request.form.get("is_5g", "No").lower() == "yes"),
            "rear_camera_mp": float(request.form.get("rear_camera_mp", 0) or 0),
            "front_camera_mp": float(request.form.get("front_camera_mp", 0) or 0),
            "internal_memory": int(request.form.get("internal_memory", 0) or 0),
            "ram": int(request.form.get("ram", 0) or 0),
            "battery": int(request.form.get("battery", 0) or 0),
            "weight": int(request.form.get("weight", 0) or 0),
            "release_year": int(request.form.get("release_year", 0) or 0),
            "days_used": int(request.form.get("days_used", 0) or 0)
        }

        raw_df = pd.DataFrame([data])
        raw_df.to_csv('raw_data.csv', mode='a', header=not os.path.exists('raw_data.csv'), index=False)

        # Validate data
        missing_cols = [col for col in num_features + cat_features if col not in raw_df.columns]
        if missing_cols:
            return jsonify({"error": f"Missing columns: {', '.join(missing_cols)}"})

        processed_data = preprocess_data(raw_df)
        prediction = model.predict(processed_data)

        final_price = round(prediction[0] * 1000)

        return render_template('index.html', predicted_price=final_price)
     else:
        return render_template('index.html')

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
