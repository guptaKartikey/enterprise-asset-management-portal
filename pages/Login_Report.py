import streamlit as st
import pandas as pd
from utils import ui_helpers
st.set_page_config(
    page_title="SAP Login Violation Dashboard",
    layout="wide"
)
st.logo("datasets/Hero_Section_Imgaes/logo.jpeg")
ui_helpers.inject_custom_css()
ui_helpers.inject_top_right_logo()
st.title("🖥️ SAP Login Violation Dashboard")
# =========================
# SESSION STATE
# =========================
if "asset_data" not in st.session_state:
    st.session_state.asset_data = None
if "login_data" not in st.session_state:
    st.session_state.login_data = None
# track uploaded files
if "last_asset_file" not in st.session_state:
    st.session_state.last_asset_file = None
if "last_login_file" not in st.session_state:
    st.session_state.last_login_file = None
# =========================
# UPLOAD
# =========================
c1,c2 = st.columns(2)
with c1:
    asset_file = st.file_uploader(
        "Upload Asset Dataset",
        type=["csv","xlsx"],
        key="asset_upload"
    )
with c2:
    login_file = st.file_uploader(
        "Upload Login Dataset",
        type=["csv","xlsx"],
        key="login_upload"
    )
def read_file(file):
    if file.name.endswith(".csv"):
        return pd.read_csv(file)
    return pd.read_excel(file, engine="calamine")
# =========================
# ASSET CLEAN
# =========================
def clean_asset(df):
    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
    )
    df=df.rename(
        columns={
            "Employee ID":"User ID",
            "User":"Employee Name",
            "Asset Tag":"Assigned Asset"
        }
    )
    for col in [
        "User ID",
        "Employee Name",
        "Department",
        "Assigned Asset",
        "Asset Type"
    ]:
        if col not in df.columns:
            df[col]="NA"
    df=df[
        [
            "User ID",
            "Employee Name",
            "Department",
            "Assigned Asset",
            "Asset Type"
        ]
    ]
    for col in df.columns:
        df[col]=(
            df[col]
            .astype(str)
            .str.strip()
        )
    def remove_decimal_zero(val):
        s = str(val).strip()
        if s.endswith(".0"):
            return s[:-2]
        return s
    df["User ID"]=df["User ID"].str.upper().apply(remove_decimal_zero)
    df["Assigned Asset"]=(
        df["Assigned Asset"]
        .str.upper()
        .apply(remove_decimal_zero)
    )
    df["Asset Type"]=(
        df["Asset Type"]
        .str.upper()
    )
    df=df[
        df["Asset Type"]
        .isin(
            [
                "LAPTOP",
                "PC",
                "DESKTOP"
            ]
        )
    ]
    df=df[
        df["User ID"].notna() &
        ~df["User ID"]
        .astype(str)
        .str.upper()
        .str.strip()
        .isin(["NAN", "", "NONE", "NA", "<NA>"])
    ]
    df=df[
        df["Assigned Asset"].notna() &
        ~df["Assigned Asset"]
        .astype(str)
        .str.upper()
        .str.strip()
        .isin(["NAN", "", "NONE", "NA", "<NA>"])
    ]
    return df.drop_duplicates()
# =========================
# LOGIN CLEAN
# =========================
def clean_login(df):
    df.columns=(
        df.columns
        .astype(str)
        .str.strip()
    )
    df=df.rename(
        columns={
            "Usr Nam":"User ID",
            "Creation Date":"Login Date",
            "Creation time of audit entry":"Login Time",
            "Terminal name":"Login Asset"
        }
    )
    df=df[
        [
            "User ID",
            "Login Date",
            "Login Time",
            "Login Asset"
        ]
    ]
    def remove_decimal_zero(val):
        s = str(val).strip()
        if s.endswith(".0"):
            return s[:-2]
        return s
    df["User ID"]=(
        df["User ID"]
        .astype(str)
        .str.upper()
        .str.strip()
        .apply(remove_decimal_zero)
        .apply(lambda x: x[1:] if str(x).startswith(('E', 'C')) and str(x)[1:].isdigit() else x)
    )
    df["Login Asset"]=(
        df["Login Asset"]
        .astype(str)
        .str.upper()
        .str.strip()
        .apply(remove_decimal_zero)
    )
    df["Login Date"]=pd.to_datetime(
        df["Login Date"],
        errors="coerce"
    )
    remove=[
        "C4517",
        "N021",
        "SAP",
        "SYSTEM",
        "ADMIN",
        "BATCH",
        "TEST"
    ]
    pattern="|".join(remove)
    df=df[
        df["User ID"].notna() &
        ~df["User ID"]
        .astype(str)
        .str.upper()
        .str.strip()
        .isin(["NAN", "", "NONE", "NA", "<NA>"])
    ]
    df=df[
        ~df["User ID"]
        .str.contains(
            pattern,
            na=False
        )
    ]
    df=df[
        df["Login Asset"].notna() &
        ~df["Login Asset"]
        .astype(str)
        .str.upper()
        .str.strip()
        .isin(
            [
                "NAN",
                "",
                "NONE",
                "NA",
                "<NA>"
            ]
        )
    ]
    return df
# =========================
# PROCESS
# =========================
if asset_file:
    if st.session_state.last_asset_file != asset_file.name:
        st.session_state.asset_data = clean_asset(
            read_file(asset_file)
        )
        st.session_state.last_asset_file = asset_file.name

if login_file:
    if st.session_state.last_login_file != login_file.name:
        st.session_state.login_data = clean_login(
            read_file(login_file)
        )
        st.session_state.last_login_file = login_file.name

if st.session_state.asset_data is not None and st.session_state.login_data is not None:
    st.success(f"📊 Active Datasets: Asset ({st.session_state.last_asset_file}) | Login ({st.session_state.last_login_file})")
    
    asset = st.session_state.asset_data
    login = st.session_state.login_data
    employee_assets = (
        asset
        .groupby("User ID")
        ["Assigned Asset"]
        .apply(set)
        .to_dict()
    )
    employee_info = (
        asset
        [
            [
                "User ID",
                "Employee Name",
                "Department"
            ]
        ]
        .drop_duplicates("User ID")
    )
    login = login.merge(
        employee_info,
        on="User ID",
        how="inner"
    )
    login["Allowed Assets"] = (
        login["User ID"]
        .map(employee_assets)
    )
    login["Valid Login"] = login.apply(
        lambda x:
        x["Login Asset"]
        in x["Allowed Assets"],
        axis=1
    )
    violation = login[
        login["Valid Login"] == False
    ].copy()
    device_owner = (
        asset
        [
            [
                "Assigned Asset",
                "Employee Name"
            ]
        ]
        .drop_duplicates("Assigned Asset")
        .set_index("Assigned Asset")
        ["Employee Name"]
        .to_dict()
    )
    
    violation["Real Login Asset Owner"] = (
        violation["Login Asset"]
        .map(device_owner)
        .fillna("Unknown")
    )
    
    violation["Employee Allowed Assets"] = (
        violation["User ID"]
        .map(
            lambda x:
            " ".join(
                employee_assets.get(x,[])
            )
        )
    )
    
    owner_assets_map = (
        asset
        .groupby("Employee Name")
        ["Assigned Asset"]
        .apply(lambda x: " ".join(set(x)))
        .to_dict()
    )
    
    violation["Assigned Assets"] = (
        violation["Real Login Asset Owner"]
        .map(owner_assets_map)
        .fillna("None")
    )

    violation["Other Asset Login Count"] = (
        violation
        .groupby(
            [
                "User ID",
                "Login Asset"
            ]
        )
        ["Login Asset"]
        .transform("count")
    )
# =========================
# SUMMARY
# =========================
    a,b,c,d = st.columns(4)
    a.metric(
        "Total Login",
        len(login)
    )
    b.metric(
        "Valid Login",
        len(login)-len(violation)
    )
    c.metric(
        "Other Asset Login",
        len(violation)
    )
    d.metric(
        "Users Impacted",
        violation["User ID"].nunique()
    )
    st.divider()
    # SEARCH SAME AS BEFORE
    x,y = st.columns(2)
    with x:
        search_by = st.selectbox(
            "Search By",
            [
                "User ID",
                "Employee Name"
            ]
        )
    with y:
        search = st.text_input(
            "Search"
        )
    result = violation.copy()
    if search:
        result=result[
            result[search_by]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]
    st.subheader(
        "Violation Details"
    )
   
    display_table = result[
        [
            "User ID",
            "Employee Name",
            "Login Asset",
            "Department",
            "Employee Allowed Assets",
            "Real Login Asset Owner",
            "Assigned Assets",
            "Other Asset Login Count"
        ]
    ].drop_duplicates()
    
    st.dataframe(
    display_table,
    use_container_width=True,
    hide_index=True
    )
    
    # =========================
    # DETAILED VIOLATION LOGS
    # =========================
    st.divider()
    st.subheader("📋 Detailed Violation Logs (Row-by-Row)")
    
    detailed_table = result[
        [
            "User ID",
            "Login Date",
            "Login Time",
            "Employee Name",
            "Login Asset",
            "Department",
            "Employee Allowed Assets",
            "Real Login Asset Owner",
            "Assigned Assets"
        ]
    ].copy()
    
    # Format Date to YYYY-MM-DD if it is datetime
    if pd.api.types.is_datetime64_any_dtype(detailed_table["Login Date"]):
        detailed_table["Login Date"] = detailed_table["Login Date"].dt.strftime("%Y-%m-%d")
        
    detailed_table = detailed_table.sort_values(by=["Employee Name", "Login Date", "Login Time"])
    
    st.dataframe(
        detailed_table,
        use_container_width=True,
        hide_index=True
    )
    
    # =========================
   # VIOLATOR INDIVIDUAL REPORT
   # =========================
    st.divider()
    st.subheader(
    "🚨 Violator Individual Details"
    )
    if not result.empty:
      violator_list = (
        result["User ID"]
        .drop_duplicates()
        .tolist()
    )
      selected_violator = st.selectbox(
        "Select Violator",
        violator_list
    )
      violator_data = result[
        result["User ID"] == selected_violator
    ]
      st.markdown(
        f"### 👤 Employee : {violator_data['Employee Name'].iloc[0]}"
    )
      col1,col2,col3 = st.columns(3)
      with col1:
        st.metric(
            "Wrong Login Count",
            len(violator_data)
        )
      with col2:
        st.metric(
            "Used Wrong Devices",
            violator_data["Login Asset"].nunique()
        )
      with col3:
        st.metric(
            "Department",
            violator_data["Department"].iloc[0]
        )
      st.markdown(
        "### 🔴 Login Violation History"
    )
      detail = violator_data[
        [
            "Login Date",
            "Login Time",
            "Login Asset",
            "Employee Allowed Assets",
            "Real Login Asset Owner",
            "Assigned Assets"
        ]
    ]
      detail = detail.rename(
        columns={
            "Login Asset":"Used Device",
            "Real Login Asset Owner":"Real Owner"
        }
    )
      st.dataframe(
        detail,
        use_container_width=True,
        hide_index=True
    )
    else:
        st.success(
          "No Violations Found"
    )
else:
    st.info(
        "Upload both files"
    )
    