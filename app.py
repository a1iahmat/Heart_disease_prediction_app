from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------
# Settings
# ---------------------------------------------------------------
APP_TITLE = "Heart Disease Prediction by Ali"
BASE_DIR = Path(__file__).parent

# Used only if the scaler does not store its own column names
DEFAULT_SCALER_COLUMNS = ["Age", "RestingBP", "Cholesterol", "MaxHR", "Oldpeak"]

st.set_page_config(page_title=APP_TITLE, page_icon="❤️", layout="centered")

st.markdown(
    """
    <style>
    .block-container {padding-top: 2rem; max-width: 900px;}
    .result-box {padding: 1.2rem; border-radius: 12px; margin-top: 1rem;}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------
# Load the 3 files (only once)
# ---------------------------------------------------------------
@st.cache_resource
def load_files():
    columns = joblib.load(BASE_DIR / "columns.pkl")
    model = joblib.load(BASE_DIR / "LogisticRegression_heart.pkl")
    scaler = joblib.load(BASE_DIR / "scaler.pkl")
    return list(columns), model, scaler


try:
    all_columns, model, scaler = load_files()
except FileNotFoundError as error:
    st.error(f"A required file is missing: {error}")
    st.stop()
except Exception as error:
    st.error(f"Could not load the model files: {error}")
    st.stop()

# The model does not use the answer column
model_columns = [c for c in all_columns if c != "HeartDisease"]
if hasattr(model, "feature_names_in_"):
    model_columns = list(model.feature_names_in_)

if hasattr(scaler, "feature_names_in_"):
    scaler_columns = list(scaler.feature_names_in_)
else:
    scaler_columns = DEFAULT_SCALER_COLUMNS

if len(model_columns) != model.n_features_in_:
    st.error("The columns file does not match the model. Please check your files.")
    st.stop()
if len(scaler_columns) != scaler.n_features_in_:
    st.error("The scaler columns do not match the scaler. Please check your files.")
    st.stop()


def as_input(data, estimator):
    """Give a DataFrame if the estimator knows column names, else a numpy array."""
    if hasattr(estimator, "feature_names_in_"):
        return data
    return data.to_numpy()


# ---------------------------------------------------------------
# Page header
# ---------------------------------------------------------------
st.title(f"❤️ {APP_TITLE}")
st.write("Fill in the patient details and click **Predict**.")

# ---------------------------------------------------------------
# Input form
# ---------------------------------------------------------------
with st.form("patient_form"):
    st.subheader("Patient details")
    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age", min_value=18, max_value=100, value=50)
        sex_label = st.selectbox("Sex", ["Male", "Female"])
        chest_pain_label = st.selectbox(
            "Chest pain type",
            [
                "ASY - No symptoms",
                "ATA - Atypical angina",
                "NAP - Non-anginal pain",
                "TA - Typical angina",
            ],
        )
        resting_bp = st.number_input(
            "Resting blood pressure (mm Hg)", min_value=50, max_value=250, value=120
        )
        cholesterol = st.number_input(
            "Cholesterol (mg/dl)", min_value=0, max_value=700, value=200
        )

    with col2:
        fasting_label = st.selectbox(
            "Fasting blood sugar", ["Below 120 mg/dl", "Above 120 mg/dl"]
        )
        resting_ecg_label = st.selectbox(
            "Resting ECG",
            [
                "Normal",
                "ST - ST-T wave abnormality",
                "LVH - Left ventricular hypertrophy",
            ],
        )
        max_hr = st.number_input(
            "Maximum heart rate", min_value=60, max_value=220, value=150
        )
        angina_label = st.selectbox("Exercise-induced angina", ["No", "Yes"])
        oldpeak = st.number_input(
            "Oldpeak (ST depression)",
            min_value=-3.0,
            max_value=7.0,
            value=1.0,
            step=0.1,
        )
        st_slope_label = st.selectbox("ST slope", ["Up", "Flat", "Down"])

    submitted = st.form_submit_button("Predict", use_container_width=True)

# ---------------------------------------------------------------
# Prediction
# ---------------------------------------------------------------
if submitted:
    # Turn the labels into the same values used in training
    raw = {
        "Age": age,
        "RestingBP": resting_bp,
        "Cholesterol": cholesterol,
        "FastingBS": 1 if fasting_label.startswith("Above") else 0,
        "MaxHR": max_hr,
        "Oldpeak": oldpeak,
        "Sex": "M" if sex_label == "Male" else "F",
        "ChestPainType": chest_pain_label.split(" - ")[0],
        "RestingECG": resting_ecg_label.split(" - ")[0],
        "ExerciseAngina": "Y" if angina_label == "Yes" else "N",
        "ST_Slope": st_slope_label,
    }

    # 1) one-row DataFrame
    df = pd.DataFrame([raw])

    # 2) one-hot encode
    df = pd.get_dummies(
        df, columns=["Sex", "ChestPainType", "RestingECG", "ExerciseAngina", "ST_Slope"]
    )

    # 3) match the training columns (missing ones become 0)
    df = df.reindex(columns=model_columns, fill_value=0).astype(float)

    # 4) scale only the columns the scaler was trained on
    df[scaler_columns] = scaler.transform(as_input(df[scaler_columns], scaler))

    # 5) predict
    probability = float(model.predict_proba(as_input(df, model))[0][1])
    is_high_risk = probability >= 0.5

    st.subheader("Result")
    if is_high_risk:
        st.error(f"⚠️ High risk of heart disease. Probability: {probability:.1%}")
    else:
        st.success(f"✅ Low risk of heart disease. Probability: {probability:.1%}")

    st.progress(min(max(probability, 0.0), 1.0))

    with st.expander("Show the data sent to the model"):
        st.dataframe(df)

st.divider()
st.caption(
    "⚠️ This app is for learning only. It is not medical advice. "
    "Please talk to a doctor for any health problem."
)