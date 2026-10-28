# Disease Prediction App

A small Streamlit app that predicts a patient outcome from hospital data using a Random Forest model.

> Educational project. It is not a medical device and must not be used to make clinical decisions.

## How it works

On first run the app reads `data01.xlsx`, cleans it, trains a Random Forest classifier (scikit-learn) and saves it to `model.pkl`. Later runs load the saved model.

Cleaning steps:

- Drop duplicate rows
- Remove outliers in `age` and `BMI` with the 1.5 x IQR rule
- Drop rows with no `outcome`, fill remaining missing values with column means
- Scale every feature from the fourth column onward to the 0 to 1 range

The form in the app collects the patient values and returns the predicted outcome.

## Run it

You need a recent Python 3.

```bash
git clone https://github.com/DrEnosh/disease-prediction-app.git
cd disease-prediction-app
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS / Linux
pip install -r requirements.txt
streamlit run app.py
```

Open the local address Streamlit prints (usually http://localhost:8501).

## Files

| File | Purpose |
| --- | --- |
| `app.py` | Streamlit app: data cleaning, model training, prediction form |
| `data01.xlsx` | Dataset used to train the model |
| `model.pkl` | Trained model, created on first run |
| `predictive_analysis.ipynb` | Notebook with the exploration and model analysis |
| `requirements.txt` | Python dependencies |

## Author

Dr. Enosh A Paulson. [LinkedIn](https://linkedin.com/in/dr-enosh) · [GitHub](https://github.com/DrEnosh)
