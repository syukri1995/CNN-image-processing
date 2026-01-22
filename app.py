import streamlit as st
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image

import os
from pathlib import Path

# =============================
# PAGE CONFIG
# =============================
st.set_page_config(
    page_title="Food Classifier",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================
# CSS STYLING
# =============================
def local_css():
    st.markdown("""
    <style>
    .main {
        background-color: #f5f5f5;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #ff4b4b;
        text-align: center;
    }
    .prediction-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        margin-bottom: 20px;
    }
    .prediction-title {
        font-size: 24px;
        font-weight: bold;
        color: #333;
    }
    .confidence-score {
        font-size: 48px;
        font-weight: bold;
        color: #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

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
# LOAD MODEL
# =============================
try:
    model = load_food_model()
except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.warning("⚠️ If you are running this locally, make sure you have pulled the model file via Git LFS.")
    model = None

class_names = ['Burger', 'Cake', 'Fried Rice', 'Pizza', 'Sushi']

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.image("https://img.icons8.com/color/96/000000/chef-hat.png", width=80)
st.sidebar.title("Food Classifier")
st.sidebar.info("This CNN model can classify food images into 5 categories.")

st.sidebar.markdown("### 📋 Categories")
for food in class_names:
    st.sidebar.markdown(f"- {food}")

st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Project Info")
st.sidebar.write("**Course:** CSC583 - AI")
st.sidebar.write("**Student:** Syukri Shamsudin")
st.sidebar.write("**Institution:** UiTM")

st.sidebar.markdown("---")
with st.sidebar.expander("❓ How to use"):
    st.write("1. Upload a food image (JPG/PNG).")
    st.write("2. Wait for the model to analyze.")
    st.write("3. View the top prediction and confidence.")

st.sidebar.caption("Built with TensorFlow & Streamlit")

# -----------------------------
# MAIN UI
# -----------------------------
st.title("🍽️ Food Image Classification")
st.markdown("### Upload a food image to get started")

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown("#### 1. Upload Image")
    uploaded_file = st.file_uploader(
        "Choose a food image...",
        type=["jpg", "jpeg", "png"]
    )

    if uploaded_file:
        img = Image.open(uploaded_file).convert("RGB")
        st.image(img, caption="Uploaded Image", use_container_width=True)

with col2:
    st.markdown("#### 2. Prediction Results")

    if uploaded_file:
        if model is None:
            st.error("⚠️ Model is not loaded. Cannot predict.")
        else:
            # Preprocess
            img_resized = img.resize((224,224))
            img_array = image.img_to_array(img_resized)
            img_array = np.expand_dims(img_array, axis=0)
            img_array = img_array / 255.0

            # Predict
            with st.spinner('Analyzing image...'):
                prediction = model.predict(img_array)
                predicted_class_idx = np.argmax(prediction)
                predicted_class = class_names[predicted_class_idx]
                confidence = float(np.max(prediction))

            # Display Top Prediction
            st.markdown(f"""
            <div class="prediction-box" role="alert" aria-live="polite">
                <div class="prediction-title">Top Prediction</div>
                <div class="confidence-score">{predicted_class}</div>
                <p>Confidence: {confidence*100:.1f}%</p>
            </div>
            """, unsafe_allow_html=True)

            if confidence > 0.8:
                st.success("High confidence prediction! 🎉")
            elif confidence > 0.5:
                st.warning("Moderate confidence. 🤔")
            else:
                st.error("Low confidence. The model is unsure. 😕")

            # Probability Chart
            st.markdown("### Class Probabilities")

            # Create DataFrame for chart
            prob_df = pd.DataFrame({
                'Category': class_names,
                'Probability': prediction[0]
            })

            # Sort for better visualization
            prob_df = prob_df.sort_values(by='Probability', ascending=False)

            st.bar_chart(
                prob_df,
                x='Category',
                y='Probability',
                color="#ff4b4b"
            )

    else:
        st.info("👈 Waiting for you to upload an image!")
        st.markdown("""
        ### I can recognize:

        *   🍔 **Burger**
        *   🍰 **Cake**
        *   🍚 **Fried Rice**
        *   🍕 **Pizza**
        *   🍣 **Sushi**

        *Upload an image from your device to see the magic happen!*
        """)
