import streamlit as st
import numpy as np
import pandas as pd
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from PIL import Image
from streamlit_option_menu import option_menu

import os
from pathlib import Path

class MockModel:
    """Mock model for testing/development without LFS files"""
    def predict(self, input_data):
        # Return dummy probabilities for 5 classes: Donut, sandwich, hot_dog, pizza, sushi
        return np.array([[0.1, 0.8, 0.05, 0.02, 0.03]])

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
        background-color: #D32F2F;
        color: white;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    h1 {
        color: #D32F2F;
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
        color: #D32F2F;
    }
    /* Gallery Styles */
    div[data-testid="stImage"] {
        border-radius: 10px;
        overflow: hidden;
    }
    div[data-testid="stImage"] img {
        border-radius: 10px;
        transition: transform 0.3s ease;
    }
    div[data-testid="stImage"]:hover img {
        transform: scale(1.02);
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
    if os.environ.get("MOCK_MODEL"):
        return MockModel()

    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    model_path = script_dir / "food_cnn_model.keras"
    
    # Check if model file exists
    if not model_path.exists():
        # Fallback for dev environment without LFS
        if os.environ.get("CI") or os.environ.get("HEADLESS"):
            return None
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

class_names = ['Donut', 'sandwich', 'hot_dog', 'pizza', 'sushi']

def show_classifier():
    # -----------------------------
    # SIDEBAR CONTENT FOR CLASSIFIER
    # -----------------------------
    st.sidebar.markdown("### 📋 Categories")
    for food in class_names:
        st.sidebar.markdown(f"- {food}")

    st.sidebar.markdown("---")
    with st.sidebar.expander("❓ How to use"):
        st.write("1. Upload a food image (JPG/PNG).")
        st.write("2. Wait for the model to analyze.")
        st.write("3. View the top prediction and confidence.")

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
            type=["jpg", "jpeg", "png"],
            help="Upload a clear photo of a single food item. Supported formats: JPG, PNG."
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

                st.toast("Analysis complete!", icon="✅")

                # Display Top Prediction
                st.markdown(f"""
                <div class="prediction-box" role="status" aria-live="polite">
                    <h2 class="prediction-title">Top Prediction</h2>
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
                    color="#D32F2F"
                )

        else:
            st.info(
                "👋 **Upload a photo to start!**\n\n"
                "I can currently recognize these 5 foods:\n"
                "* 🍩 Donut\n"
                "* 🥪 Sandwich\n"
                "* 🌭 Hot Dog\n"
                "* 🍕 Pizza\n"
                "* 🍣 Sushi"
            )

def show_gallery():
    st.title("🖼️ Training Dataset Gallery")

    # Init session state
    if 'view_mode' not in st.session_state:
        st.session_state.view_mode = 'grid'
        st.session_state.current_image_index = 0
        st.session_state.current_image_list = []

    dataset_path = Path("dataset/train")
    if not dataset_path.exists():
        st.error(f"Dataset directory not found at {dataset_path.absolute()}")
        return

    # Gather categories
    try:
        categories = sorted([d.name for d in dataset_path.iterdir() if d.is_dir() and not d.name.startswith('_')])
    except Exception as e:
        st.error(f"Error reading dataset: {e}")
        return

    # Sidebar controls for gallery
    with st.sidebar:
        st.markdown("### 🖼️ Gallery Settings")
        selected_category = st.selectbox("Select Category", ["All"] + categories)
        num_images = st.selectbox("Images to show", [10, 20, 50, 100], index=0)

    # Filter images
    image_paths = []
    if selected_category == "All":
        for cat in categories:
            cat_path = dataset_path / cat
            # Get jpg/png/jpeg
            files = sorted(list(cat_path.glob("*.jpg")) + list(cat_path.glob("*.png")) + list(cat_path.glob("*.jpeg")))
            # For "All", we limit total? Or per category?
            # User said "show how many images can be shown as default is 10".
            # If I show 10 from EACH category, that's 50. If I show 10 TOTAL, that's 2 per cat.
            # I'll assume "per category" when All is selected, to be generous, or "Top N total".
            # Let's do 10 per category if All, or just simple collection.
            image_paths.extend(files[:num_images])
    else:
        cat_path = dataset_path / selected_category
        files = sorted(list(cat_path.glob("*.jpg")) + list(cat_path.glob("*.png")) + list(cat_path.glob("*.jpeg")))
        image_paths.extend(files[:num_images])

    # -----------------------------
    # GRID MODE
    # -----------------------------
    if st.session_state.view_mode == 'grid':
        st.session_state.current_image_list = [str(p) for p in image_paths]

        if not image_paths:
            st.warning("No images found.")
            return

        cols = st.columns(4)
        for i, img_path in enumerate(image_paths):
            with cols[i % 4]:
                # Use a container for better spacing
                with st.container():
                    st.image(str(img_path), use_container_width=True)
                    # Button to open fullscreen
                    if st.button("🔍 View", key=f"btn_{i}", use_container_width=True):
                        st.session_state.view_mode = 'fullscreen'
                        st.session_state.current_image_index = i
                        st.rerun()

    # -----------------------------
    # FULLSCREEN MODE
    # -----------------------------
    elif st.session_state.view_mode == 'fullscreen':
        if not st.session_state.current_image_list:
            st.warning("No images loaded.")
            if st.button("Back to Gallery"):
                st.session_state.view_mode = 'grid'
                st.rerun()
            return

        # Ensure index is within bounds
        total = len(st.session_state.current_image_list)
        if st.session_state.current_image_index >= total:
            st.session_state.current_image_index = total - 1
        if st.session_state.current_image_index < 0:
            st.session_state.current_image_index = 0

        idx = st.session_state.current_image_index
        img_path = st.session_state.current_image_list[idx]

        # Navigation UI
        col_prev, col_img, col_next = st.columns([1, 10, 1])

        with col_prev:
            # Spacer to center vertical button approximately
            for _ in range(10): st.write("")
            if idx > 0:
                if st.button("◀️", key="prev_btn", help="Previous image"):
                    st.session_state.current_image_index -= 1
                    st.rerun()
            else:
                st.button("◀️", disabled=True, key="prev_btn_disabled", help="No previous image")

        with col_img:
            # Display the main image
            st.image(img_path, caption=f"Image {idx+1} of {total}: {Path(img_path).name}", use_container_width=True)

            # Exit Button Centered
            c1, c2, c3 = st.columns([4, 2, 4])
            with c2:
                if st.button("Exit Fullscreen", key="exit_btn", use_container_width=True, help="Return to grid view"):
                    st.session_state.view_mode = 'grid'
                    st.rerun()

        with col_next:
            for _ in range(10): st.write("")
            if idx < total - 1:
                if st.button("▶️", key="next_btn", help="Next image"):
                    st.session_state.current_image_index += 1
                    st.rerun()
            else:
                st.button("▶️", disabled=True, key="next_btn_disabled", help="No more images")

# -----------------------------
# MAIN APP NAVIGATION
# -----------------------------
with st.sidebar:
    st.sidebar.image("https://img.icons8.com/color/96/000000/chef-hat.png", width=80)
    st.sidebar.title("Food Classifier")

    selected = option_menu(
        menu_title="Navigation",
        options=["Classifier", "Dataset Gallery"],
        icons=['house', 'images'],
        menu_icon="cast",
        default_index=0,
        styles={
            "nav-link-selected": {"background-color": "#D32F2F"},
        }
    )

if selected == "Classifier":
    # Reset view mode when switching tabs so gallery starts fresh?
    # Or keep state? Keeping state is better UX usually.
    show_classifier()
elif selected == "Dataset Gallery":
    show_gallery()

# -----------------------------
# GLOBAL SIDEBAR INFO
# -----------------------------
st.sidebar.markdown("---")
st.sidebar.markdown("### ℹ️ Project Info")
st.sidebar.write("**Course:** CSC583 - AI")
st.sidebar.write("**Student:** Syukri Shamsudin")
st.sidebar.write("**Institution:** UiTM")
st.sidebar.caption("Built with TensorFlow & Streamlit")
