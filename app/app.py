import streamlit as st
import pickle
import os
import pandas as pd
import sys

# =========================================================
# PATH FIX (IMPORTANT)
# =========================================================
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

# =========================================================
# IMPORT FROM SRC
# =========================================================
from src.data_cleaning import clean_data
from src.recommender import get_similar_houses
from src.prediction import predict_price
from src.utils import property_category, generate_insights
from src.analytics import (
    price_distribution,
    bhk_analysis,
    correlation_heatmap
)

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="Smart Real Estate AI",
    page_icon="🏡",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

.block-container {
    padding-top: 2rem;
}

h1, h2, h3, h4 {
    color: white;
}

.metric-card {
    background: linear-gradient(135deg, #1f2937, #111827);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0px 4px 20px rgba(0,0,0,0.4);
    text-align: center;
}

.metric-value {
    font-size: 32px;
    font-weight: bold;
    color: #60A5FA;
}

.metric-label {
    font-size: 16px;
    color: #D1D5DB;
}

.prediction-card {
    background: linear-gradient(135deg, #111827, #1F2937);
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0px 4px 25px rgba(0,0,0,0.5);
}

.insight-box {
    background-color: #1E293B;
    padding: 14px;
    border-radius: 12px;
    margin-bottom: 10px;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# TITLE
# =========================================================
st.markdown("""
# 🏡 Smart Real Estate Intelligence System
### AI-Powered House Price Prediction & Analytics Platform
""")

st.markdown("---")

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_data():

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.join(BASE_DIR, "../data/Bengaluru_House_Data.csv")

    df = pd.read_csv(DATA_PATH)
    df = clean_data(df)

    return df


df = load_data()

# =========================================================
# LOAD MODELS
# =========================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "../models")

lr = pickle.load(open(os.path.join(MODEL_DIR, "lr.pkl"), "rb"))
ridge = pickle.load(open(os.path.join(MODEL_DIR, "ridge.pkl"), "rb"))
rf = pickle.load(open(os.path.join(MODEL_DIR, "rf.pkl"), "rb"))

models = {
    "Linear Regression": lr,
    "Ridge Regression": ridge,
    "Random Forest": rf
}

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("⚙ AI Controls")

model_name = st.sidebar.selectbox(
    "Select Prediction Model",
    list(models.keys())
)

model = models[model_name]

# =========================================================
# KPI CARDS
# =========================================================
st.subheader("📊 Market Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Properties", len(df))
col2.metric("Average Price", f"{df['price'].mean():.2f} L")
col3.metric("Maximum Price", f"{df['price'].max():.2f} L")

st.markdown("---")

# =========================================================
# ANALYTICS DASHBOARD
# =========================================================
st.subheader("📈 Real Estate Analytics Dashboard")

tab1, tab2, tab3 = st.tabs([
    "Price Distribution",
    "BHK Analysis",
    "Correlation"
])

with tab1:
    st.plotly_chart(price_distribution(df), use_container_width=True)

with tab2:
    st.plotly_chart(bhk_analysis(df), use_container_width=True)

with tab3:
    st.plotly_chart(correlation_heatmap(df), use_container_width=True)

st.markdown("---")

# =========================================================
# PREDICTION SECTION
# =========================================================
st.subheader("🏠 AI House Price Prediction")

col1, col2 = st.columns([1, 1])

# INPUT
with col1:

    st.markdown("### Enter Property Details")

    sqft = st.slider("Square Feet", 100, 10000, 1200)
    bhk = st.slider("BHK", 1, 10, 2)
    bath = st.slider("Bathrooms", 1, 10, 2)

# OUTPUT
with col2:

    st.markdown('<div class="prediction-card">', unsafe_allow_html=True)
    st.markdown("### 🤖 AI Prediction Engine")

    if st.button("Predict Property Price 🚀"):

        try:
            prediction, luxury = predict_price(
                model,
                sqft,
                bhk,
                bath
            )

            st.success(f"🏡 Estimated Price: ₹ {prediction:.2f} Lakhs")
            st.markdown("### 🏡 Similar Houses You May Like")

            similar_df = get_similar_houses(
                df,
                sqft,
                bhk,
                bath,
                n=5
            )
            st.dataframe(similar_df, use_container_width=True)
            # INSIGHTS
            st.markdown("### 🧠 AI Insights")

            insights = generate_insights(sqft, bhk, luxury)

            for insight in insights:
                st.markdown(f"✔ {insight}")

            # CATEGORY
            st.markdown("### 🏘 Property Category")

            category = property_category(luxury, sqft)

            if luxury == 1:
                st.success(category)
            elif sqft > 2000:
                st.info(category)
            else:
                st.warning(category)

        except Exception as e:
            st.error(f"Error: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("---")

st.markdown("""
<center>
### 💡 Smart Real Estate Intelligence Platform 🚀
</center>
""", unsafe_allow_html=True)