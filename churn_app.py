import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="Telecom Customer Churn Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Telecom Customer Churn Dashboard")

# ----------------------------------------
# Load Data
# ----------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("churn-bigml-80.csv")

df = load_data()

# ----------------------------------------
# Sidebar Filters
# ----------------------------------------
st.sidebar.header("Filters")

area = st.sidebar.multiselect(
    "Area Code",
    options=df["Area code"].unique(),
    default=df["Area code"].unique()
)

intl_plan = st.sidebar.multiselect(
    "International Plan",
    options=df["International plan"].unique(),
    default=df["International plan"].unique()
)

voice_plan = st.sidebar.multiselect(
    "Voice Mail Plan",
    options=df["Voice mail plan"].unique(),
    default=df["Voice mail plan"].unique()
)

churn = st.sidebar.multiselect(
    "Churn",
    options=df["Churn"].unique(),
    default=df["Churn"].unique()
)

filtered_df = df[
    (df["Area code"].isin(area)) &
    (df["International plan"].isin(intl_plan)) &
    (df["Voice mail plan"].isin(voice_plan)) &
    (df["Churn"].isin(churn))
]

# ----------------------------------------
# KPIs
# ----------------------------------------
st.subheader("Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Customers", len(filtered_df))

with col2:
    churn_rate = (filtered_df["Churn"]=="Yes").mean()*100
    st.metric("Churn Rate", f"{churn_rate:.2f}%")

with col3:
    st.metric(
        "Average Day Minutes",
        f"{filtered_df['Total day minutes'].mean():.2f}"
    )

with col4:
    st.metric(
        "Average Customer Service Calls",
        f"{filtered_df['Customer service calls'].mean():.2f}"
    )

st.divider()

# ----------------------------------------
# Charts
# ----------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.histogram(
        filtered_df,
        x="Churn",
        color="Churn",
        title="Customer Churn Count"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.box(
        filtered_df,
        x="Churn",
        y="Total day minutes",
        color="Churn",
        title="Day Minutes vs Churn"
    )

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.scatter(
        filtered_df,
        x="Total day minutes",
        y="Total eve minutes",
        color="Churn",
        title="Day Minutes vs Evening Minutes"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.histogram(
        filtered_df,
        x="Customer service calls",
        color="Churn",
        barmode="group",
        title="Customer Service Calls"
    )

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------

col1, col2 = st.columns(2)

with col1:

    fig = px.pie(
        filtered_df,
        names="International plan",
        title="International Plan Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:

    fig = px.pie(
        filtered_df,
        names="Voice mail plan",
        title="Voice Mail Plan Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------
# Correlation Heatmap
# ----------------------------------------

st.subheader("Correlation Heatmap")

numeric_df = filtered_df.select_dtypes(include="number")

corr = numeric_df.corr()

fig = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="RdBu_r",
    title="Correlation Matrix"
)

st.plotly_chart(fig, use_container_width=True)

# ----------------------------------------
# Data Table
# ----------------------------------------

st.subheader("Filtered Dataset")

st.dataframe(filtered_df, use_container_width=True)

# ----------------------------------------
# Download Button
# ----------------------------------------

csv = filtered_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="filtered_churn.csv",
    mime="text/csv"
)