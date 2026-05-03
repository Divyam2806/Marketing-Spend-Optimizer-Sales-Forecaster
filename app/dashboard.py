import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
ROOT = os.path.dirname(os.path.dirname(__file__))
import streamlit as st
import pandas as pd
from src.data_generator import generate_dataset
from src.model import load_model, train_model, save_model
from src.optimizer import optimize_budget
from src.visualizer import plot_eda, plot_optimization, plot_scenarios
from src.simulator import simulate_scenarios

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Marketing Spend Optimizer",
    page_icon="📈",
    layout="wide"
)

# ── Load Model & Data ─────────────────────────────────────────
@st.cache_resource
def get_model_and_data():
    """Load model and data once at startup."""
    df = generate_dataset(n=200)
    model_path = os.path.join(ROOT, 'data', 'model.joblib')
    if os.path.exists(model_path):
        model = load_model(model_path)
    else:
        model, features, metrics, test_data = train_model(df)
        save_model(model, model_path)
    features = [col for col in df.columns if col.endswith('_spend')]
    return model, features, df
model, features, df = get_model_and_data()

# ── Header ────────────────────────────────────────────────────
st.title("📈 Marketing Spend Optimizer & Sales Forecaster")
st.markdown("Optimize your marketing budget allocation using regression-based predictions.")
st.divider()

# ── Sidebar ───────────────────────────────────────────────────
st.sidebar.header(" Configuration")
total_budget = st.sidebar.slider(
    "Total Budget ($K)",
    min_value=100,
    max_value=2000,
    value=700,
    step=50
)

# ── EDA Section ───────────────────────────────────────────────
st.header(" Exploratory Data Analysis")
fig_eda = plot_eda(df)
st.pyplot(fig_eda)
st.divider()

# ── Optimizer Section ─────────────────────────────────────────
st.header(" Optimal Budget Allocation")
st.markdown(f"Finding the best split for a **${total_budget}K** budget to maximize revenue.")

optimal_spend, optimal_revenue = optimize_budget(model, features, total_budget)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Optimal Allocation")
    for channel, spend in optimal_spend.items():
        label = channel.replace('_spend', '').capitalize()
        pct = spend / total_budget * 100
        st.metric(label=label, value=f"${spend:,.1f}K", delta=f"{pct:.1f}%")

with col2:
    fig_opt = plot_optimization(optimal_spend, optimal_revenue)
    st.pyplot(fig_opt)

st.success(f" Predicted Revenue: ${optimal_revenue:,.0f}K  |  ROI: {(optimal_revenue - total_budget) / total_budget * 100:.1f}%")
st.divider()

# ── Scenario Simulator Section ────────────────────────────────
st.header(" Custom Scenario Simulator")
st.markdown("Manually set spend per channel and see predicted revenue instantly.")

channel_spends = []
cols = st.columns(len(features))

for i, feature in enumerate(features):
    label = feature.replace('_spend', '').capitalize()
    with cols[i]:
        spend = st.slider(
            f"{label} ($K)",
            min_value=0,
            max_value=total_budget,
            value=total_budget // len(features),
            step=10
        )
        channel_spends.append(spend)

total_allocated = sum(channel_spends)
custom_input = pd.DataFrame([channel_spends], columns=features)
custom_prediction = model.predict(custom_input)[0]

st.metric("Total Allocated", f"${total_allocated:,.0f}K")
st.metric("Predicted Revenue", f"${custom_prediction:,.0f}K")
st.metric("Predicted ROI", f"{(custom_prediction - total_allocated) / total_allocated * 100:.1f}%")

st.divider()

# ── Scenario Comparison ───────────────────────────────────────
st.header(" Scenario Comparison")
scenarios_df = simulate_scenarios(model, features, total_budget)
fig_scenarios = plot_scenarios(scenarios_df)
st.pyplot(fig_scenarios)