import streamlit as st
import pandas as pd

def preprocess_data(data):
    # Placeholder function for preprocessing
    return data  # Replace with actual preprocessing steps

def predict_price(processed_data):
    # Placeholder function for ML model prediction
    return 999.99  # Replace with actual model prediction logic

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
        normalized_used_price = st.number_input("Normalized Used Price", min_value=0.0, step=0.1)
        normalized_new_price = st.number_input("Normalized New Price", min_value=0.0, step=0.1)
        
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
            "normalized_used_price": [normalized_used_price],
            "normalized_new_price": [normalized_new_price]
        })
        
        processed_data = preprocess_data(data)
        predicted_price = predict_price(processed_data)
        
        st.write("### Generated DataFrame:")
        st.dataframe(data)
        
        st.write("### Predicted Price:")
        st.write(f"$ {predicted_price:.2f}")

if __name__ == "__main__":
    main()
