# ==========================================
# 🇮🇳 Indian Economy Streamlit Dashboard
# ==========================================

# Import Libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Indian Economy Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==========================================
# Dashboard Title
# ==========================================

st.title("🇮🇳 Indian Middle-Class Financial Stress Dashboard")

st.markdown("""
## 📌 Project Objective

This project analyzes the financial health of Indian middle-class households using economic indicators such as:

- Inflation
- Savings behavior
- Cost of living
- Rent burden
- Employment stability
- Financial stress

The goal is to identify economically vulnerable states and understand affordability challenges across India.
""")

# ==========================================
# Load Dataset
# ==========================================

@st.cache_data
def load_data():
    df = pd.read_csv("indian_economy_realworld_dataset.csv")
    return df

# Load data
df = load_data()

# ==========================================
# Feature Engineering
# ==========================================

# Expense to Income Ratio
df["Expense_Income_Ratio"] = (
    df["Monthly_Expense"] /
    df["Monthly_Income"]
) * 100

# Savings Rate
df["Savings_Rate"] = (
    df["Savings"] /
    df["Monthly_Income"]
) * 100

# Rent Burden
df["Rent_Burden_%"] = (
    df["Rent"] /
    df["Monthly_Income"]
) * 100

# Real Income
df["Real_Income"] = (
    df["Monthly_Income"] /
    (1 + df["Inflation_Rate"] / 100)
)

# Financial Stress Score
df["Financial_Stress_Score"] = (
    df["Expense_Income_Ratio"] * 0.5 +
    df["Inflation_Rate"] * 2 -
    df["Savings_Rate"] * 0.3
)

# ==========================================
# Sidebar Filters
# ==========================================

st.sidebar.header("📌 Filters")

selected_states = st.sidebar.multiselect(
    "Select States",
    options=df["State"].unique(),
    default=df["State"].unique()
)

# Filter dataset
filtered_df = df[
    df["State"].isin(selected_states)
]

# ==========================================
# KPI Calculations
# ==========================================

avg_income = filtered_df["Monthly_Income"].mean()
avg_expense = filtered_df["Monthly_Expense"].mean()
avg_savings = filtered_df["Savings"].mean()
avg_inflation = filtered_df["Inflation_Rate"].mean()

# ==========================================
# KPI Cards
# ==========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Average Income",
    f"₹{avg_income:,.0f}"
)

col2.metric(
    "Average Expense",
    f"₹{avg_expense:,.0f}"
)

col3.metric(
    "Average Savings",
    f"₹{avg_savings:,.0f}"
)

col4.metric(
    "Inflation Rate",
    f"{avg_inflation:.2f}%"
)
st.subheader("📈 National Economic Summary")

highest_income_state = df.loc[
    df["Monthly_Income"].idxmax(),
    "State"
]

highest_savings_state = df.loc[
    df["Savings_Rate"].idxmax(),
    "State"
]

highest_stress_state = df.loc[
    df["Financial_Stress_Score"].idxmax(),
    "State"
]

st.write(f" Highest Income State: {highest_income_state}")

st.write(f" Best Savings State: {highest_savings_state}")

st.write(f" Highest Financial Stress State: {highest_stress_state}")
# ==========================================
# Display Dataset
# ==========================================

st.subheader("📊 Dataset")

st.dataframe(filtered_df)

# ==========================================
# Income vs Expense Chart
# ==========================================

st.subheader("💰 Income vs Expense Analysis")

fig1, ax1 = plt.subplots(figsize=(12,6))

x = np.arange(len(filtered_df))
width = 0.35

ax1.bar(
    x - width/2,
    filtered_df["Monthly_Income"],
    width,
    label="Income"
)

ax1.bar(
    x + width/2,
    filtered_df["Monthly_Expense"],
    width,
    label="Expense"
)

ax1.set_xticks(x)
ax1.set_xticklabels(
    filtered_df["State"],
    rotation=45
)

ax1.set_title("Monthly Income vs Expense")
ax1.set_ylabel("Amount")
ax1.legend()

st.pyplot(fig1)

# ==========================================
# Savings Rate Analysis
# ==========================================

st.subheader("🏦 Savings Rate Analysis")

fig2, ax2 = plt.subplots(figsize=(10,6))

sns.barplot(
    x="Savings_Rate",
    y="State",
    data=filtered_df,
    palette="viridis",
    ax=ax2
)

ax2.set_title("Savings Rate by State")

st.pyplot(fig2)


# ==========================================
# Expense Distribution
# ==========================================

st.subheader("🥧 Expense Distribution")

expense_data = [
    filtered_df["Rent"].sum(),
    filtered_df["Healthcare"].sum(),
    filtered_df["Education"].sum()
]

labels = [
    "Rent",
    "Healthcare",
    "Education"
]

fig_pie, ax_pie = plt.subplots(figsize=(8,8))

ax_pie.pie(
    expense_data,
    labels=labels,
    autopct="%1.1f%%"
)

st.pyplot(fig_pie)

# ==========================================
# Rent Burden Analysis
# ==========================================

st.subheader("🏠 Rent Burden Analysis")

fig3, ax3 = plt.subplots(figsize=(10,6))

sns.barplot(
    x="Rent_Burden_%",
    y="State",
    data=filtered_df,
    palette="magma",
    ax=ax3
)

ax3.set_title("Rent Burden Percentage")

st.pyplot(fig3)

# ==========================================
# Financial Stress Analysis
# ==========================================

st.subheader("⚠️ Financial Stress Score")

fig4, ax4 = plt.subplots(figsize=(10,6))

sns.barplot(
    x="Financial_Stress_Score",
    y="State",
    data=filtered_df,
    palette="coolwarm",
    ax=ax4
)

ax4.set_title("Financial Stress by State")

st.pyplot(fig4)

# ==========================================
# Correlation Heatmap
# ==========================================

st.subheader("📈 Economic Correlation Heatmap")

fig5, ax5 = plt.subplots(figsize=(12,8))

corr = filtered_df.select_dtypes(
    include=np.number
).corr()

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax5
)

ax5.set_title("Correlation Matrix")

st.pyplot(fig5)

# ==========================================
# Top Performing States
# ==========================================

st.subheader("🏆 Top Performing States")

best_savings = filtered_df.sort_values(
    by="Savings_Rate",
    ascending=False
).head(5)

st.write("### Top 5 States by Savings Rate")

st.dataframe(
    best_savings[
        ["State", "Savings_Rate"]
    ]
)

# ==========================================
# Real-World Business Insights
# ==========================================

st.subheader("💡 Real-World Business Insights")

st.success(
    "Metro cities show higher salaries but also higher financial pressure due to rising living costs."
)

st.warning(
    "High inflation reduces purchasing power and affects middle-class savings."
)

st.info(
    "Rent burden is one of the biggest contributors to financial stress in urban states."
)

st.error(
    "Lower-income states are more vulnerable to economic shocks and inflation."
)

# ==========================================


# ==========================================
# Download Dataset
# ==========================================

csv = filtered_df.to_csv(index=False)

st.download_button(
    label=" Download Dataset",
    data=csv,
    file_name="indian_economy_realworld_dataset.csv",
    mime="text/csv"
)
# Footer
# ==========================================

st.markdown("---")

st.markdown(
    "Created using Pandas, NumPy, Matplotlib, Seaborn & Streamlit"
)