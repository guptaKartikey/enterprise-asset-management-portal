import streamlit as st
import pandas as pd
from utils import ui_helpers


st.set_page_config(
    page_title="Enterprise Asset Dashboard",
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


st.title("📊 Enterprise Asset Dashboard")

# ====================================
# IN USE & IT STOCK LOGIC
# ====================================

# Employee ID available = IN Use
in_use_df = df[df["Employee ID"].notna()]

# Employee ID blank = IT Stock
it_stock_df = df[df["Employee ID"].isna()]

# ====================================
# KPI CARDS
# ====================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Assets", len(df))

with col2:
    st.metric("IN Use Assets", len(in_use_df))

with col3:
    st.metric("IT Stock Assets", len(it_stock_df))

with col4:
    st.metric(
        "Employees",
        in_use_df["Employee ID"].nunique()
    )

st.divider()

# ====================================
# DEPARTMENT WISE ASSET TYPE
# ====================================

st.subheader("Department Wise Asset Distribution")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### IN Use Assets")

    dept_in_use = pd.pivot_table(
        in_use_df,
        index="Department",
        columns="Asset Type",
        aggfunc="size",
        fill_value=0
    )

    st.bar_chart(dept_in_use)

    st.dataframe(
        dept_in_use.reset_index(),
        use_container_width=True
    )

with col2:

    st.markdown("### IT Stock Assets")

    dept_stock = pd.pivot_table(
        it_stock_df,
        index="Department",
        columns="Asset Type",
        aggfunc="size",
        fill_value=0
    )

    st.bar_chart(dept_stock)

    st.dataframe(
        dept_stock.reset_index(),
        use_container_width=True
    )

st.divider()

# ====================================
# LOCATION WISE ASSET TYPE
# ====================================

st.subheader("Location Wise Asset Distribution")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### IN Use Assets")

    loc_in_use = pd.pivot_table(
        in_use_df,
        index="Location",
        columns="Asset Type",
        aggfunc="size",
        fill_value=0
    )

    st.bar_chart(loc_in_use)

    st.dataframe(
        loc_in_use.reset_index(),
        use_container_width=True
    )

with col2:

    st.markdown("### IT Stock Assets")

    loc_stock = pd.pivot_table(
        it_stock_df,
        index="Location",
        columns="Asset Type",
        aggfunc="size",
        fill_value=0
    )

    st.bar_chart(loc_stock)

    st.dataframe(
        loc_stock.reset_index(),
        use_container_width=True
    )

st.divider()

# ====================================
# ASSET TYPE SUMMARY
# ====================================

st.subheader("Asset Type Summary")

asset_summary = (
    df.groupby("Asset Type")
    .size()
    .reset_index(name="Count")
    .sort_values("Count", ascending=False)
)

st.bar_chart(
    asset_summary.set_index("Asset Type")
)

st.dataframe(
    asset_summary,
    use_container_width=True
)

st.divider()

# ====================================
# TOP 10 LOCATIONS
# ====================================

st.subheader("Top Locations by Asset Count")

top_locations = (
    df.groupby("Location")
    .size()
    .reset_index(name="Count")
    .sort_values("Count", ascending=False)
    .head(10)
)

st.bar_chart(
    top_locations.set_index("Location")
)

st.dataframe(
    top_locations,
    use_container_width=True
)

st.divider()

