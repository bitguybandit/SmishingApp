# SmishingApp
Explainable SMS phishing (smishing) detector: web app that classifies messages  as scam or legit using NLP (TF-IDF + Naive Bayes / Logistic Regression) and  explains its verdict via red-flag detection. Academic case study (ITPD 6 - AI 1).

# Smishing Detector — Explainable SMS Phishing Classification

A web-based prototype that classifies text messages as **scam or legitimate**
using Natural Language Processing (supervised machine learning), and explains
its verdict by surfacing the red flags it detected.

Built as the software deliverable for a research-based case study (IMRAD format)
in Artificial Intelligence 1 (ITPD 6).

## Features

- 🔍 **Message classification** — paste any SMS, get a scam/legitimate verdict
  with a confidence score
- ⚠️ **Red-flag explanations** — rule-based detection of:
  - Suspicious URLs
  - Urgency / pressure language ("blocked", "expire", "urgent", "immediately")
  - Bank / e-wallet / courier impersonation (GCash, BDO, BPI, Maya, LBC, J&T)
  - Money requests and phone-number contact attempts
- 🧪 **Demo buttons** — one-click sample scam and legitimate messages

## AI Technique

Supervised text classification:
1. **TF-IDF vectorization** (1–2 word n-grams) converts messages into numerical features
2. **Multinomial Naive Bayes** classifier (Logistic Regression used as comparison model)
3. Rule-based red-flag scanner provides human-readable explanations

## Repository Structure

├── app.py                  # Streamlit web application
├── model.pkl               # Trained classifier (joblib)
├── vectorizer.pkl          # Fitted TF-IDF vectorizer (joblib)
├── requirements.txt        # Python dependencies
├── training_notebook.ipynb # Google Colab training + evaluation pipeline
├── data/
│   └── (datasets used - see Data Sources)
└── README.md


## Setup & Installation

Requires **Python 3.10+**.

```bash
# 1. Clone the repository
git clone https://github.com/bitguybandit/SmishingApp.git
cd smishing-detector

# 2. (Recommended) Create a virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`.

### requirements.txt

```
streamlit
scikit-learn
joblib
pandas
```

# 4. Run the app
streamlit run app.py
The app opens at http://localhost:8501.
