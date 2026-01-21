import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

import os
from pathlib import Path

# =============================
# CACHE MODEL LOADING
# =============================
@st.cache_resource
def load_food_model():
    """Load and cache the CNN model"""
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    model_path = script_dir / "food_cnn_model.keras"
    
    # Check if model file exists
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    
    return load_model(str(model_path))

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Food Classifier",
    page_icon="🍽️",
    layout="centered"
)

# =============================
# LOAD MODEL
# =============================
try:
    model = load_food_model()
except FileNotFoundError as e:
    st.error(f"❌ Error: {e}")
    st.stop()

class_names = ['burger', 'cake', 'fried_rice', 'pizza', 'sushi']

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🍔 Food CNN Classifier")
st.sidebar.write("CSC583 Group Project")
st.sidebar.write("CNN-based Image Classification")
st.sidebar.markdown("---")  
st.sidebar.write("NBCS2305A - Artificial Intelligence")
st.sidebar.write("UiTM Cawangan Shah Alam")
st.sidebar.markdown("---") 

# -----------------------------
# MAIN UI
# -----------------------------
st.title("🍽️ Food Image Classification")
st.info("""
**Supported Foods:** Burger 🍔, Cake 🍰, Fried Rice 🍚, Pizza 🍕, Sushi 🍣
Upload an image of one of these foods for the best results.
""")

uploaded_file = st.file_uploader(
    "📤 Upload Image",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Uploaded Image", width=300)

        img_resized = img.resize((224,224))
        img_array = image.img_to_array(img_resized)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0

        with st.spinner("Analyzing image..."):
            prediction = model.predict(img_array)

        predicted_class = class_names[np.argmax(prediction)]
        confidence = float(np.max(prediction))

        st.subheader("🔍 Prediction Result")
        st.success(f"**{predicted_class.upper()}**")
        st.progress(confidence)
        st.caption(f"Confidence: {confidence*100:.2f}%")
        st.balloons()
