
import streamlit as st
import pandas as pd
import os
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from io import BytesIO

# Streamlit Page Configuration
st.set_page_config(page_title="💿 Data Sweeper - AI Powered", layout="wide")

# Dark Mode Toggle
dark_mode = st.sidebar.checkbox("🌙 Dark Mode")
if dark_mode:
    st.markdown(
        """
        <style>
        body {background-color: #121212; color: white;}
        .stApp {background-color: #121212;}
        </style>
        """, unsafe_allow_html=True
    )

# App Header
st.title("💿 Data Sweeper - AI Powered")
st.write("Transform and clean your datasets effortlessly! 🚀")

# File Uploader
uploaded_files = st.file_uploader("📂 Upload CSV or Excel files:", type=["csv", "xlsx"], accept_multiple_files=True)

# Process Each File
if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        # Read CSV or Excel
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue  # Skip unsupported files

        # File Info
        st.subheader(f"📄 File: {file.name}")
        st.write(f"**Size:** {file.size / 1024:.2f} KB")
        
        # Data Preview
        st.write("🔍 Data Preview:")
        st.dataframe(df.head())

        # Data Summary
        st.subheader("📊 Data Summary & Insights")
        st.write(df.describe())

        # Detect Missing Values
        st.subheader("⚠️ Missing Values Report")
        missing_values = df.isnull().sum()
        st.write(missing_values[missing_values > 0])

        # AI-Powered Data Cleaning
        st.subheader("🛠 AI-Powered Data Cleaning")

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button(f"🚀 Auto Remove Duplicates - {file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("✅ Duplicates removed!")

        with col2:
            if st.button(f"🧹 Auto Fill Missing Values - {file.name}"):
              df.fillna(df.select_dtypes(include=['number']).mean(), inplace=True)
              st.success("✅ Missing values filled!")

        with col3:
            if st.button(f"🔍 Detect & Remove Outliers - {file.name}"):
                numeric_cols = df.select_dtypes(include=["number"])
                z_scores = ((numeric_cols - numeric_cols.mean()) / numeric_cols.std()).abs()
                df = df[(z_scores < 3).all(axis=1)]
                st.success("✅ Outliers removed!")

        # Data Type Transformation
        st.subheader("🛠 Data Type Transformation")
        st.write("🔄 Convert text columns to numerical where applicable.")
        for col in df.select_dtypes(include="object").columns:
            if st.checkbox(f"Convert {col} to numeric"):
                df[col] = pd.to_numeric(df[col], errors='coerce')
                st.success(f"✅ {col} converted to numeric.")

        # Data Visualization
        st.subheader("📊 Advanced Data Visualization")

        chart_type = st.selectbox("📈 Choose Chart Type", ["Bar Chart", "Pie Chart", "Histogram", "Correlation Heatmap"])
        col_x = st.selectbox("X-axis", df.columns)
        col_y = st.selectbox("Y-axis", df.select_dtypes(include="number").columns)

        if st.button("Generate Chart"):
            if chart_type == "Bar Chart":
                fig = px.bar(df, x=col_x, y=col_y, title=f"{col_x} vs {col_y}")
            elif chart_type == "Pie Chart":
                fig = px.pie(df, names=col_x, title=f"Distribution of {col_x}")
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=col_x, title=f"Histogram of {col_x}")
            elif chart_type == "Correlation Heatmap":
                plt.figure(figsize=(10, 6))
                sns.heatmap(df.corr(), annot=True, cmap="coolwarm", fmt=".2f")
                st.pyplot(plt)
                fig = None  # No need to return a figure for matplotlib

            if fig:
                st.plotly_chart(fig)

        # File Conversion Options
        st.subheader("🔄 File Conversion")
        conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        # Convert & Download
        if st.button(f"📥 Convert & Download {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            else:
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"

            buffer.seek(0)
            st.download_button(
                label=f"⬇ Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

# Success Message
st.success("🎉 All files processed successfully!")










