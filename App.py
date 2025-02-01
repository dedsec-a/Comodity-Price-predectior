import streamlit as st
import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder
# Load the model
model = pickle.load(open("model.pkl", "rb"))
ohe = OneHotEncoder(handle_unknown= 'ignore')

def preprocess_data(data):
    # Perform preprocessing
    df = pd.DataFrame(data)
    ohe.fit(df[["device_brand", "os"]])
    df["os_type"] =  pd.get_dummies(df["os"])
    df["4g"] = df["4g"].map({'yes': 1, 'no': 0}).astype(int)
    df["5g"] = df["5g"].map({'yes': 1, 'no': 0}).astype(int)
    df_encoded = np.array(df)

    return df_encoded
 # Replace with actual preprocessing steps

def predict_price(data):

    # Predict the price
    prediction = model.predict(data)

    
    return prediction  # Replace with actual model prediction logic

def main():
    st.title("Mobile Specification Form")
    
    device_brands = [
        "Others", "Samsung", "Huawei", "LG", "Lenovo", "ZTE", "Xiaomi", "Oppo", "Asus", "Alcatel", "Micromax", "Vivo", "Honor", "HTC", "Nokia", "Motorola", "Sony", "Meizu", "Gionee", "Acer", "XOLO", "Panasonic", "Realme", "Apple", "Lava", "Celkon", "Spice", "Karbonn", "Coolpad", "BlackBerry", "Microsoft", "OnePlus", "Google", "Infinix"
    ]
    
    with st.form("mobile_form"):
        device_brand = st.selectbox("Device Brand", device_brands)
        os = st.selectbox("Operating System", ["Android", "iOS", "Other"])
        screen_size = st.number_input("Screen Size (in inches)", min_value=4.0, max_value=7.5, step=0.1)
        is_4g = st.radio("4G Support", ["Yes", "No"])
        is_5g = st.radio("5G Support", ["Yes", "No"])
        rear_camera_mp = st.number_input("Rear Camera (MP)", min_value=1.0, max_value=200.0, step=0.1)
        front_camera_mp = st.number_input("Front Camera (MP)", min_value=1.0, max_value=100.0, step=0.1)
        internal_memory = st.number_input("Internal Memory (GB)", min_value=4, max_value=1024, step=1)
        ram = st.number_input("RAM (GB)", min_value=1, max_value=32, step=1)
        battery = st.number_input("Battery Capacity (mAh)", min_value=1000, max_value=10000, step=100)
        weight = st.number_input("Weight (grams)", min_value=50, max_value=500, step=1)
        release_year = st.number_input("Release Year", min_value=2000, max_value=2025, step=1)
        days_used = st.number_input("Days Used", min_value=0, step=1)
     
        
        submit = st.form_submit_button("Submit")
    
    if submit:
        data = pd.DataFrame({
            "device_brand": [device_brand],
            "os": [os],
            "screen_size": [screen_size],
            "4g": [is_4g == "Yes"],
            "5g": [is_5g == "Yes"],
            "rear_camera_mp": [rear_camera_mp],
            "front_camera_mp": [front_camera_mp],
            "internal_memory": [internal_memory],
            "ram": [ram],
            "battery": [battery],
            "weight": [weight],
            "release_year": [release_year],
            "days_used": [days_used],
            
        })
        
      
        
        st.write("### Generated DataFrame:")
        st.dataframe(data)

        # Preprocess the data
        data = preprocess_data(data)
        st.write("### Preprocessed Data:")
        st.write(data)
        # Predict the price
        prediction = predict_price(data)
        st.write("### Predicted Price:")
        st.write(prediction)

       

if __name__ == "__main__":
    main()
