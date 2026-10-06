import streamlit as st
import pandas as pd
from utils import ui_helpers

st.set_page_config(
    page_title="Enterprise Asset & SAP Portal",
    page_icon="datasets/Hero_Section_Imgaes/logo.png",
    layout="wide"
)
st.logo("datasets/Hero_Section_Imgaes/logo.png")
ui_helpers.inject_custom_css()
ui_helpers.inject_top_right_logo()

st.title("💻 Enterprise Asset Management Portal")

# Hero section slideshow
st.components.v1.html(ui_helpers.get_hero_carousel_html(), height=290)
st.markdown("<br>", unsafe_allow_html=True)


# ==========================
# CLEAN DATA
# ==========================

@st.cache_data
def clean_data(file):

    if file.name.endswith(".csv"):
        df = pd.read_csv(file)

    else:
        df = pd.read_excel(file, engine="calamine")


    df = df.dropna(how="all")

    df = df.drop_duplicates()

    df.columns = (
        df.columns
        .str.strip()
    )

    return df



# ==========================
# UPLOAD
# ==========================

st.sidebar.header("📂 Upload Dataset")


uploaded_file = st.sidebar.file_uploader(
    "Upload CSV / Excel",
    type=["csv","xlsx"]
)


if uploaded_file:


    df = clean_data(uploaded_file)


    # STORE DATA FOR ALL PAGES
    st.session_state["df"] = df


    st.success(
        "Dataset uploaded successfully"
    )



# ==========================
# CHECK
# ==========================

if "df" not in st.session_state:

    st.warning(
        "Please upload dataset first"
    )

    st.stop()



df = st.session_state["df"]



# ==========================
# KPI
# ==========================

c1,c2,c3,c4 = st.columns(4)


c1.metric(
    "Total Assets",
    len(df)
)


c2.metric(
    "Employees",
    df["Employee ID"].nunique()
    if "Employee ID" in df.columns else 0
)


c3.metric(
    "Departments",
    df["Department"].nunique()
    if "Department" in df.columns else 0
)


c4.metric(
    "Locations",
    df["Location"].nunique()
    if "Location" in df.columns else 0
)



st.divider()


st.subheader("Dataset Preview")


st.dataframe(
    df,
    use_container_width=True
)



csv = df.to_csv(index=False)


st.download_button(
    "⬇ Download Clean Dataset",
    csv,
    "clean_dataset.csv",
    "text/csv"
)