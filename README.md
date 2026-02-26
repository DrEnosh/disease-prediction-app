# Disease Prediction App

A machine learning web application built with Streamlit that predicts disease risk based on patient hospital data.

## Overview
This application uses a Random Forest Classifier trained on real clinical data to predict the likelihood of a specific disease outcome. The interface allows users to input patient demographics and medical history to get an instant risk assessment.

## Features
*   **Interactive UI:** Built with Streamlit for a clean, user-friendly experience.
*   **Machine Learning Model:** Utilizes a Random Forest model (`scikit-learn`) for accurate predictions.
*   **Data Processing:** Handles missing values, outliers, and scales features automatically.

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd Disease_Prediction_App
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On macOS/Linux
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
2. Open your web browser and navigate to the local URL provided in the terminal (usually `http://localhost:8501`).

## Files in this Repository
*   `app.py`: The main Streamlit application script.
*   `data01.xlsx`: The clinical dataset used for training the model.
*   `requirements.txt`: List of Python dependencies.
*   `model.pkl`: The serialized trained Random Forest model (generated on first run).
*   `Predictive_analysis(regression) (2).ipynb`: Jupyter notebook for model exploration and analysis.
