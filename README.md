# Salary Predictor — Render Deployment Guide

A Flask API serving a Linear Regression model for fresher placement salary prediction.

---

## Project Structure

```
salary-predictor/
├── app.py              ← Flask inference API
├── requirements.txt    ← Python dependencies
├── index.html          ← Frontend UI (open locally or host separately)
├── salary_model.pkl    ← Trained LinearRegression model  ← YOU MUST ADD THIS
└── scaler.pkl          ← Fitted StandardScaler           ← YOU MUST ADD THIS
```

---

## Step 1 — Export your model files from Colab

Run this in your Colab notebook (already in your script):

```python
import joblib
joblib.dump(model, "salary_model.pkl")
joblib.dump(scaler, "scaler.pkl")

from google.colab import files
files.download("salary_model.pkl")
files.download("scaler.pkl")
```

Place both `.pkl` files in the same folder as `app.py`.

---

## Step 2 — Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: salary prediction API"
git remote add origin https://github.com/YOUR_USERNAME/salary-predictor.git
git push -u origin main
```

> Make sure `.pkl` files are committed too (they're small, Git is fine with them).

---

## Step 3 — Deploy on Render (Free Tier)

1. Go to [https://render.com](https://render.com) → Sign up / Log in
2. Click **New → Web Service**
3. Connect your GitHub repo
4. Fill in these settings:

| Field | Value |
|---|---|
| **Name** | salary-predictor (or anything) |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Instance Type** | Free |

5. Click **Create Web Service**

Render will build and deploy. Takes ~2-3 minutes first time.

Your API will be live at:
```
https://salary-predictor.onrender.com   (or whatever name you chose)
```

---

## Step 4 — Use the Frontend

Open `index.html` in any browser (double-click it, no server needed).

Paste your Render URL into the **Backend URL** field at the top, fill in the candidate details, and click **Predict Salary**.

---

## API Reference

### `GET /`
Health check.

```json
{ "status": "ok", "message": "Salary Prediction API is running." }
```

### `POST /predict`

**Request body (JSON):**

```json
{
  "cgpa": 7.5,
  "college_tier": 2,
  "python_skill": 1,
  "dsa_skill": 0,
  "ml_skill": 1,
  "web_dev_skill": 0,
  "communication_score": 65,
  "aptitude_score": 60,
  "internships": 1,
  "projects": 2,
  "backlogs": 0,
  "resume_score": 75
}
```

**Response:**

```json
{
  "predicted_salary_lpa": 9.45,
  "input_received": { ... }
}
```

---

## Notes on Free Tier

- **Cold starts:** Render's free tier spins down after ~15 minutes of inactivity. The first request after idle may take 30–60 seconds. Subsequent requests are fast.
- **No persistent storage:** The `.pkl` files are loaded at startup from your repo. Don't try to write files during runtime on free tier.
- **Memory:** Free tier gives 512 MB RAM — more than enough for this model.

---

## Local Testing (optional)

```bash
pip install flask flask-cors joblib numpy scikit-learn gunicorn
python app.py
```

Then open `index.html` and set the Backend URL to `http://localhost:5000`.
