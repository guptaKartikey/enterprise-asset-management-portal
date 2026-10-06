import streamlit as st
import pandas as pd
from utils import ui_helpers

st.set_page_config(
    page_title="Enterprise Reports",
    page_icon="datasets/Hero_Section_Imgaes/logo.png",
    layout="wide"
)
st.logo("datasets/Hero_Section_Imgaes/logo.png")
ui_helpers.inject_custom_css()
ui_helpers.inject_top_right_logo()

if "df" not in st.session_state:

    st.warning(
        "Upload dataset from Home page"
    )

    st.stop()


df = st.session_state["df"]

st.title("📑 Enterprise Asset Reports")



col1, col2, col3 = st.columns(3)

with col1:
    department = st.selectbox(
        "Select Department",
        ["All"] +
        sorted(
            df["Department"]
            .dropna()
            .unique()
            .tolist()
        )
    )

with col2:
    asset_type_list = []
    if "Asset Type" in df.columns:
        asset_type_list = sorted(df["Asset Type"].dropna().astype(str).unique().tolist())
    asset_type = st.selectbox(
        "Select Asset Type",
        ["All"] + asset_type_list
    )

with col3:
    location_list = []
    if "Location" in df.columns:
        location_list = sorted(df["Location"].dropna().astype(str).unique().tolist())
    location = st.selectbox(
        "Select Location",
        ["All"] + location_list
    )

report = df.copy()

if department != "All":
    report = report[report["Department"] == department]

if "Asset Type" in report.columns and asset_type != "All":
    report = report[report["Asset Type"] == asset_type]

if "Location" in report.columns and location != "All":
    report = report[report["Location"] == location]



st.dataframe(
    report,
    use_container_width=True
)



csv=report.to_csv(index=False)



st.download_button(
    "⬇ Download Report",
    csv,
    "report.csv",
    "text/csv"
)