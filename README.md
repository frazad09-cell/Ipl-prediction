# 🏏 IPL AI Winner Predictor

A Streamlit + Machine Learning web app that predicts the likely winner of an IPL match using historical match data, team selection, venue, toss winner, and toss decision.

## ✨ Features

- Modern interactive Streamlit UI
- Team-vs-team match setup
- Venue and toss inputs
- Winning probability for both teams
- Prediction confidence
- Personalized favourite-team message
- User profile sidebar
- Animated prediction progress
- Historical IPL dataset included

## 🧠 Tech Stack

- Python
- Pandas
- Scikit-learn / trained ML pipeline
- Streamlit
- Pickle model serialization

## 📁 Project Structure

```text
Ipl-prediction/
├── app.py
├── ipl_winner_model.pkl
├── data/
│   └── ipl_matches.csv
├── requirements.txt
└── README.md
```

## ▶️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The app expects `ipl_winner_model.pkl` in the project root.

## ⚠️ Disclaimer

This project uses historical IPL data and machine learning for educational purposes. Predictions are estimates and do not guarantee actual match results.
