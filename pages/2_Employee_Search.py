import streamlit as st
import pandas as pd
from utils import ui_helpers


st.set_page_config(
    page_title="Enterprise Employee Search",
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



st.title("🔍 Advanced Employee Search")



col1,col2 = st.columns([1,3])


with col1:

    search_type = st.selectbox(
        "Search By",
        [
            "Employee Name",
            "Employee ID",
            "Asset Tag"
        ]
    )


with col2:

    search_value = st.text_input(
        "Enter Value"
    )



filtered = df.copy()



if search_value:


    if search_type=="Employee ID":

        def clean_id(val):
            s = str(val).strip()
            if s.endswith(".0"):
                return s[:-2]
            return s

        filtered = df[
            df["Employee ID"]
            .astype(str)
            .str.strip()
            .apply(clean_id)
            ==
            search_value.strip()
        ]


    elif search_type=="Employee Name":

        filtered = df[
            df["User"]
            .astype(str)
            .str.contains(
                search_value,
                case=False,
                na=False
            )
        ]


    elif search_type=="Asset Tag":

        filtered = df[
            df["Asset Tag"]
            .astype(str)
            .str.contains(
                search_value,
                case=False,
                na=False
            )
        ]



st.write(
    f"Records Found: {len(filtered)}"
)


st.dataframe(
    filtered,
    use_container_width=True
)



if not filtered.empty:

    st.divider()

    st.subheader("👤 Employee Profile Summary")
    
    row = filtered.iloc[0]
    
    # Define common employee columns
    profile_cols = ["Employee ID", "User", "Department", "Designation", "Section", "Location", "Email", "Mobile"]
    available_cols = [c for c in profile_cols if c in filtered.columns]
    
    # Split into two columns for better UI
    pc1, pc2 = st.columns(2)
    half = (len(available_cols) + 1) // 2
    
    with pc1:
        for col in available_cols[:half]:
            val = row[col] if not pd.isna(row[col]) else "N/A"
            st.markdown(f"**{col}:** {val}")
            
    with pc2:
        for col in available_cols[half:]:
            val = row[col] if not pd.isna(row[col]) else "N/A"
            st.markdown(f"**{col}:** {val}")

    st.divider()
    st.subheader(f"📦 Assigned Assets ({len(filtered)})")
    
    # Define asset specific columns to show
    asset_cols = ["Asset Tag", "Asset Type", "Asset Category", "Asset State", "Product Make/Model", "Serial Number"]
    available_asset_cols = [c for c in asset_cols if c in filtered.columns]
    
    # If standard asset columns are not found, fallback to showing all other columns
    if not available_asset_cols:
        available_asset_cols = [c for c in filtered.columns if c not in available_cols]
        
    st.dataframe(
        filtered[available_asset_cols].reset_index(drop=True),
        use_container_width=True
    )