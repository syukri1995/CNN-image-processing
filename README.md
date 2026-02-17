# 🍔 Food CNN Image Classification

A deep learning-based food image classification system using Convolutional Neural Networks (CNN) built with TensorFlow/Keras and deployed with Streamlit.

## 📋 Project Overview

This project implements a CNN model to classify food images into 5 categories:
- 🍩 **Donut**
- 🥪 **Sandwich**
- 🌭 **Hot Dog**
- 🍕 **Pizza**
- 🍣 **Sushi**

The model achieves accurate classification through a deep learning architecture trained on custom food image datasets.

## ✨ Features

- **Real-time Image Classification**: Upload food images and get instant predictions
- **High Accuracy**: CNN model trained on diverse food datasets
- **User-Friendly Interface**: Built with Streamlit for easy interaction
- **Confidence Score**: Shows prediction confidence percentage
- **Model Caching**: Optimized performance with `@st.cache_resource`
- **Support for Multiple Formats**: Accepts JPG, JPEG, and PNG images

## 🚀 Quick Start

### Prerequisites

- Python 3.13
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/syukri1995/CNN-image-processing.git
   cd CNN-image-processing
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ensure the model file exists**
   
   The trained model `food_cnn_model.keras` should be in the project root directory. If not, train the model using the notebook in `model/cnn.ipynb`.

### Running the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📂 Project Structure

```
Food_cnn_project/
├── app.py                      # Main Streamlit application
├── food_cnn_model.keras        # Trained CNN model (Git LFS)
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── model/
│   └── cnn.ipynb              # Model training notebook
├── dataset/
│   ├── train/                 # Training images
│   ├── Donut/
│   ├── Sandwich/
│   ├── hot_dog/
│   ├── pizza/
│   └── sushi/    
└── report/                     # Project reports
```

## 🧠 Model Architecture

The CNN model consists of:
- **Convolutional Layers**: Extract spatial features from images
- **MaxPooling Layers**: Reduce dimensionality and computational complexity
- **Dense Layers**: Fully connected layers for classification
- **Dropout**: Regularization to prevent overfitting
- **Softmax Activation**: Multi-class probability distribution

### Model Configuration
- **Input Shape**: 224x224x3 (RGB images)
- **Number of Classes**: 5
- **Optimizer**: Adam
- **Loss Function**: Categorical Crossentropy
- **Epochs**: 15
- **Batch Size**: 32

## 📊 Dataset

The dataset contains food images organized into 5 categories with training and test splits:
- Images are resized to 224x224 pixels
- Data augmentation applied during training (rotation, zoom, horizontal flip)
- 80-20 train-validation split

## 🛠️ Technologies Used

- **TensorFlow/Keras**: Deep learning framework
- **Streamlit**: Web application framework
- **NumPy**: Numerical computing
- **Pillow (PIL)**: Image processing
- **scikit-learn**: Machine learning utilities
- **Matplotlib & Seaborn**: Data visualization

## 📖 Usage

1. Launch the Streamlit app
2. Upload a food image (JPG, JPEG, or PNG)
3. View the prediction and confidence score
4. The model will classify the image into one of the 5 food categories

## 🎓 Academic Information

**Course**: CSC583 - Artificial Intelligence  
**Program**: NBCS2305A  
**Institution**: UiTM Cawangan Shah Alam  
**Project Type**: Group Project

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!

## 📝 License

This project is developed for educational purposes as part of a university course project.

## 👥 Authors

- Syukri Shamsudin ([@syukri1995](https://github.com/syukri1995))

## 🙏 Acknowledgments

- UiTM Shah Alam for providing educational resources
- TensorFlow and Keras documentation
- Streamlit community for excellent tutorials

---

**Note**: The model file (`food_cnn_model.keras`) is stored using Git LFS due to its large size.
