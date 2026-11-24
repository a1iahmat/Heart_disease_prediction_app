# ❤️ Heart Disease Prediction by Ali

![Python](https://img.shields.io/badge/Python-3.14-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.7.2-orange)
![Model](https://img.shields.io/badge/Model-Logistic%20Regression-green)

A simple web app that predicts if a person has a **low risk** or a **high risk** of heart disease. The user fills in a few health details, and a trained **Logistic Regression** model gives the result with a probability.

> ⚠️ **Disclaimer:** This project is for learning and demo only. It is **not medical advice**. Always talk to a doctor for any health problem.

---

## 🔗 Live Demo

https://a1iahmat-heart-disease-prediction-app-app-3ct5sd.streamlit.app/

---

## ✨ Features

- Clean and simple web page built with Streamlit
- Easy form: sliders, drop-down lists and number boxes
- Shows **Low risk** or **High risk** with the probability (in %)
- Shows a progress bar for the risk probability
- Shows the final data sent to the model (for transparency)
- Clear error messages if a model file is missing
- Model files are loaded only once (fast, uses caching)

---

## 🧠 How It Works

```
User input  →  One-row DataFrame  →  One-hot encoding  →  Match training columns
            →  Scale number columns  →  Logistic Regression  →  Risk + probability
```

1. **Input:** The user enters the patient details in the form.
2. **DataFrame:** The input is turned into a one-row pandas DataFrame.
3. **One-hot encoding:** Text columns (Sex, ChestPainType, RestingECG, ExerciseAngina, ST_Slope) are converted to 0/1 columns.
4. **Column matching:** The data is reindexed to the exact training columns saved in `columns.pkl` (missing columns are filled with 0). This keeps the column order the same as in training.
5. **Scaling:** The numeric columns are scaled with the saved scaler (`scaler.pkl`).
6. **Prediction:** The saved model gives the probability of heart disease.
   If the probability is **50% or more**, the app shows **High risk**. Otherwise it shows **Low risk**.

---

## 🧾 Input Features

| Feature | What the user selects | Type |
|---|---|---|
| Age | Slider (18 to 100) | Number |
| Sex | Male / Female | Category |
| ChestPainType | ASY / ATA / NAP / TA | Category |
| RestingBP | Resting blood pressure (mm Hg) | Number |
| Cholesterol | Cholesterol (mg/dl) | Number |
| FastingBS | Fasting blood sugar above 120 mg/dl (Yes / No) | Binary |
| RestingECG | Normal / ST / LVH | Category |
| MaxHR | Maximum heart rate | Number |
| ExerciseAngina | Exercise-induced angina (Yes / No) | Binary |
| Oldpeak | ST depression value | Number |
| ST_Slope | Up / Flat / Down | Category |

**Target (what the model predicts):** `HeartDisease` (0 = no, 1 = yes). It is not an input in the app.

### Columns the model uses (15 columns)

`Age`, `RestingBP`, `Cholesterol`, `FastingBS`, `MaxHR`, `Oldpeak`, `Sex_M`, `ChestPainType_ATA`, `ChestPainType_NAP`, `ChestPainType_TA`, `RestingECG_Normal`, `RestingECG_ST`, `ExerciseAngina_Y`, `ST_Slope_Flat`, `ST_Slope_Up`

The first category of each text feature is dropped during training (`drop_first`). So `Sex = F`, `ChestPainType = ASY`, `RestingECG = LVH`, `ExerciseAngina = N` and `ST_Slope = Down` are shown by all-zero columns.

---

## 📁 Project Structure

```
ml pkl/
│
├── app.py                          # Streamlit web app
├── columns.pkl                     # Training column names (joblib)
├── LogisticRegression_heart.pkl    # Trained Logistic Regression model (joblib)
├── scaler.pkl                      # Trained scaler (joblib)
├── requirements.txt                # Python packages needed
└── README.md                       # This file
```

---

## 🛠️ Tech Stack

- **Python**
- **Streamlit** for the web interface
- **pandas** for data handling and one-hot encoding
- **scikit-learn** (Logistic Regression and scaler)
- **joblib** to save and load the model files

---

## 🚀 Run Locally (Windows PowerShell)

**1. Open the project folder**

```powershell
cd "E:\ali\ml pkl"
```

**2. Create a virtual environment (first time only)**

```powershell
python -m venv .venv
```

**3. Activate it**

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.\.venv\Scripts\Activate.ps1
```

**4. Install the packages**

```powershell
python -m pip install -r requirements.txt
```

**5. Start the app**

```powershell
python -m streamlit run app.py
```

The app opens at `http://localhost:8501`.
Press `Ctrl + C` in PowerShell to stop it.

---

## ☁️ Deploy on Streamlit Community Cloud (Free)

1. Push these files to a **public GitHub repository**: `app.py`, `columns.pkl`, `LogisticRegression_heart.pkl`, `scaler.pkl`, `requirements.txt`, `README.md`.
   Do **not** upload the `.venv` folder.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app** and choose your repository and branch.
4. Set **Main file path** to `app.py`.
5. Click **Deploy** and wait a few minutes.
6. Copy the app link and paste it in the **Live Demo** section above.

---

## ⚠️ Important: Pickle Version Warning

The model and scaler files are saved with **scikit-learn 1.7.2**. If the app runs with a different version, Python can show an `InconsistentVersionWarning`. This can break the app or give wrong results.

For this reason `requirements.txt` pins `scikit-learn==1.7.2`. If you train the model again with another version, update this line to match.

Also, only load `.pkl` files that you trust, because pickle files can run code when they are loaded.

---

## ✅ Quick Test Checklist

- [ ] The app opens without errors
- [ ] All inputs work (slider, drop-down lists, number boxes)
- [ ] A healthy example (young age, normal values) shows a prediction
- [ ] A risky example (older age, high BP, exercise angina = Yes, ST slope = Flat) shows a higher probability
- [ ] The probability is between 0% and 100%
- [ ] The disclaimer is visible at the bottom

---

## 📊 Model Details

| Item | Details |
|---|---|
| Algorithm | Logistic Regression |
| Scaled columns | Number columns (the scaler uses 5 features) |
| Model input columns | 15 |
| Decision threshold | 0.5 |
| Dataset | _add your dataset name and link here_ |
| Accuracy / Recall / ROC-AUC | _add your test results here_ |

---

## ⚠️ Limitations

- The model is trained on a small public-style dataset and may not work well for all people.
- It uses only the 11 listed health features.
- It is a learning project and must **not** be used for real medical decisions.

---

## 🔮 Future Improvements

- Compare more models (Random Forest, XGBoost) and choose the best one
- Add model explanation (for example SHAP) to show why a result is high or low
- Add input checks and helpful hints for each field
- Add automatic tests for the prediction code
- Save the model and the preprocessing steps in one scikit-learn `Pipeline` to avoid column mistakes

---

## 👤 Author

**Ali**
GitHub: _add your GitHub link here_
LinkedIn: _add your LinkedIn link here_
