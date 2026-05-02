# 📊 AI Demand Forecasting & Chatbot System

## 🚀 Project Overview
This project builds an end-to-end AI system to analyze sales data, forecast demand, and provide insights through an interactive chatbot interface.

It combines:
- Data analysis
- Machine learning forecasting
- Interactive visualization
- GenAI-powered chatbot

---

## 📂 Project Structure
FINAL_PROJECT/
│
├── data/ # Raw, interim, processed datasets
├── notebooks/ # Phase-wise analysis (1–11)
├── src/ # Core logic (EDA, models, forecasting)
├── models/ # Saved ML models
├── reports/ # Charts, tables, documents
├── dashboard/ # Streamlit chatbot UI
└── archive/ # Backup files


---

## ⚙️ Features

- 📊 Exploratory Data Analysis (EDA)
- 🔗 Dataset merging and validation
- 🧠 Feature engineering (lags, rolling stats)
- 🤖 Machine learning models:
  - Linear Regression
  - Random Forest
  - Gradient Boosting
- 📈 Time-series forecasting
- 📉 Model evaluation & cross-validation
- 💬 AI-powered chatbot (Streamlit UI)

---

## 📊 Key Insights

- Sales show fluctuating weekly patterns
- Certain products dominate total sales
- Categories are unevenly distributed
- Forecast model captures demand trends effectively

---

## 🤖 Chatbot Capabilities

You can ask:
- "Show top products"
- "Category sales"
- "Forecast TE001"
- "Show forecast chart"

The chatbot returns:
- Tables
- Charts
- Forecast results

---

## 🛠️ Tech Stack

- Python
- Pandas, NumPy
- Scikit-learn
- Matplotlib
- Streamlit
- FastAPI (optional backend)

---

## ▶️ How to Run

### 1. Clone repo
```bash
git clone https://github.com/Classicalstracker/Demand_Project_Final-Project.git
cd Demand_Project_Final-Project
2. Activate environment
venv\Scripts\activate
3. Install dependencies
pip install -r requirements.txt
4. Run dashboard
python -m streamlit run dashboard/app.py
