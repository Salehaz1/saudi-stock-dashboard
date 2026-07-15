import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Saudi Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

# --------------------------------------------------
# Custom CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp{
    background: linear-gradient(to right,#050816,#0B1120);
    color:white;
}

section[data-testid="stSidebar"]{
    background:#0d1117;
}

h1{
    color:#00E5FF;
    text-align:center;
}

h2,h3{
    color:#4FC3F7;
}

div[data-testid="metric-container"]{
    background:#161B22;
    border:1px solid #30363D;
    padding:20px;
    border-radius:15px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

df = pd.read_csv("clean_data.csv")

df.columns = df.columns.str.strip()

# Convert date if available
if "date" in df.columns:
    df["date"] = pd.to_datetime(df["date"])

# --------------------------------------------------
# Sidebar
# --------------------------------------------------

st.sidebar.title("📊 Dashboard Filters")

# Sector Filter
if "sectoer" in df.columns:

    sector = st.sidebar.multiselect(
        "Select Sector",
        options=sorted(df["sectoer"].unique()),
        default=sorted(df["sectoer"].unique())
    )

    df = df[df["sectoer"].isin(sector)]

# Company Filter
if "symbol" in df.columns:

    company = st.sidebar.multiselect(
        "Select Company",
        options=sorted(df["symbol"].unique()),
        default=sorted(df["symbol"].unique())
    )

    df = df[df["symbol"].isin(company)]

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📈 Saudi Stock Market Dashboard")

st.write("Interactive Dashboard for Saudi Stock Exchange (Tadawul)")

st.markdown("---")

# --------------------------------------------------
# KPIs
# --------------------------------------------------

col1,col2,col3,col4 = st.columns(4)

if "symbol" in df.columns:
    col1.metric("Companies", df["symbol"].nunique())

if "close" in df.columns:
    col2.metric("Average Close", round(df["close"].mean(),2))

if "high" in df.columns:
    col3.metric("Highest Price", round(df["high"].max(),2))

if "volume" in df.columns:
    col4.metric("Total Volume", f"{int(df['volume'].sum()):,}")

st.markdown("---")

# --------------------------------------------------
# Line Chart
# --------------------------------------------------

if "date" in df.columns and "close" in df.columns and "symbol" in df.columns:

    st.subheader("📉 Stock Closing Prices Over Time")

    fig = px.line(
        df,
        x="date",
        y="close",
        color="symbol"
    )

    fig.update_layout(
        paper_bgcolor="#050816",
        plot_bgcolor="#050816",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Bar Chart
# --------------------------------------------------

if "sectoer" in df.columns and "close" in df.columns:

    left,right = st.columns(2)

    with left:

        st.subheader("Average Close Price by Sector")

        avg = df.groupby("sectoer")["close"].mean().reset_index()

        fig = px.bar(
            avg,
            x="sectoer",
            y="close",
            color="close",
            color_continuous_scale="Turbo"
        )

        fig.update_layout(
            paper_bgcolor="#050816",
            plot_bgcolor="#050816",
            font_color="white"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:

        st.subheader("Close Price Distribution")

        fig = px.box(
            df,
            x="sectoer",
            y="close",
            color="sectoer"
        )

        fig.update_layout(
            paper_bgcolor="#050816",
            plot_bgcolor="#050816",
            font_color="white"
        )

        st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Scatter Plot
# --------------------------------------------------

if all(col in df.columns for col in ["open","close","volume","sectoer"]):

    st.subheader("Open Price vs Close Price")

    fig = px.scatter(
        df,
        x="open",
        y="close",
        color="sectoer",
        size="volume",
        hover_name="symbol"
    )

    fig.update_layout(
        paper_bgcolor="#050816",
        plot_bgcolor="#050816",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Pie Chart
# --------------------------------------------------

if "sectoer" in df.columns:

    st.subheader("Companies by Sector")

    pie = df["sectoer"].value_counts().reset_index()
    pie.columns = ["Sector","Count"]

    fig = px.pie(
        pie,
        values="Count",
        names="Sector",
        hole=.45
    )

    fig.update_layout(
        paper_bgcolor="#050816",
        font_color="white"
    )

    st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Heatmap
# --------------------------------------------------

st.subheader("Correlation Heatmap")

corr = df.select_dtypes(include="number").corr()

fig = px.imshow(
    corr,
    text_auto=True,
    color_continuous_scale="Turbo",
    aspect="auto"
)

fig.update_layout(
    paper_bgcolor="#050816",
    plot_bgcolor="#050816",
    font_color="white"
)

st.plotly_chart(fig, use_container_width=True)

# --------------------------------------------------
# Data Preview
# --------------------------------------------------

st.subheader("Dataset Preview")

st.dataframe(df, use_container_width=True)

# --------------------------------------------------
# Summary Statistics
# --------------------------------------------------

st.subheader("Summary Statistics")

st.dataframe(df.describe(), use_container_width=True)

# --------------------------------------------------
# Insights
# --------------------------------------------------

st.markdown("---")
st.header("📊 Key Insights")

col1, col2 = st.columns(2)

with col1:

    if "close" in df.columns:
        st.success(f"""
### Stock Overview

- **Average Close Price:** {df["close"].mean():.2f}

- **Highest Close Price:** {df["close"].max():.2f}

- **Lowest Close Price:** {df["close"].min():.2f}
""")

    if "symbol" in df.columns:
        st.info(f"""
### Companies

- **Total Companies:** {df["symbol"].nunique()}
""")

with col2:

    if "sectoer" in df.columns and "close" in df.columns:

        sector_avg = df.groupby("sectoer")["close"].mean()

        st.warning(f"""
### Sector Performance

- **Highest Average Close Price:**
**{sector_avg.idxmax()}**

- **Lowest Average Close Price:**
**{sector_avg.idxmin()}**
""")

    if "open" in df.columns and "symbol" in df.columns:

        highest_open = df.loc[df["open"].idxmax()]

        st.success(f"""
### Top Company

- **Highest Opening Price:** {highest_open["symbol"]}

- **Opening Price:** {highest_open["open"]:.2f}
""")