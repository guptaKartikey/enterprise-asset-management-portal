import streamlit as st
import pandas as pd
import io
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from utils import ui_helpers

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Enterprise SAP Usage Analysis",
    page_icon="datasets/Hero_Section_Imgaes/logo.png",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.logo("datasets/Hero_Section_Imgaes/logo.png")
ui_helpers.inject_custom_css()
ui_helpers.inject_top_right_logo()

# ─────────────────────────────────────────────
#  CUSTOM CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
.header-container {
    background: linear-gradient(90deg, #003d66, #005b8e, #0078b8);
    border-radius: 14px;
    padding: 22px 32px;
    margin-bottom: 24px;
    box-shadow: 0 4px 18px rgba(0,120,184,0.18);
}
.header-container h1 { color: #ffffff; font-size: 2rem; font-weight: 700; margin: 0; }
.header-container p { color: rgba(255,255,255,0.82); font-size: 0.95rem; margin: 6px 0 0; }
[data-testid="stDataFrame"] iframe { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
  <h1>🔐 Enterprise SAP Usage Analysis Dashboard</h1>
  <p>Generate exact Summary Tables with dynamic multi-month logs, Dialog user filtering, and Department-wise drill-downs.</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def read_file(f):
    if f.name.lower().endswith(".csv"):
        return pd.read_csv(f)
    return pd.read_excel(f, engine="calamine")

def strip_cols(df):
    df.columns = df.columns.astype(str).str.strip()
    return df

def _pick(cols, candidates, fallback_idx=None):
    for c in candidates:
        for actual_c in cols:
            if c.lower() in actual_c.lower():
                return actual_c
    return cols[fallback_idx] if fallback_idx is not None and fallback_idx < len(cols) else None

def normalise_id(series):
    # Optimize by parsing only unique values, dramatically speeds up large Series
    s = series.astype(str)
    unique_vals = s.unique()
    cleaned = pd.Series(unique_vals).str.strip().str.upper().str.replace(r"\.0$", "", regex=True)
    return s.map(dict(zip(unique_vals, cleaned)))

# ─────────────────────────────────────────────
#  SIDEBAR UPLOADS
# ─────────────────────────────────────────────
def reset_analysis():
    if 'analysis_run' in st.session_state:
        st.session_state['analysis_run'] = False

with st.sidebar:
    st.markdown("## 📂 Upload Data")
    
    st.markdown("**① SAP User List**")
    user_file = st.file_uploader("Upload Master User List", type=["xlsx", "csv"], key="user_upload", on_change=reset_analysis)
    
    st.markdown("**② User Access List**")
    access_file = st.file_uploader("Upload Role/Tcode Access", type=["xlsx", "csv"], key="access_upload", on_change=reset_analysis)
    
    st.markdown("**③ SM20 Audit Logs**")
    sm20_files = st.file_uploader("Upload SM20 Logs (Select Multiple)", type=["xlsx", "csv"], key="sm20_upload", accept_multiple_files=True, on_change=reset_analysis)
    
    st.markdown("---")
    st.markdown("**④ Date Range for Analysis**")
    default_from = st.session_state.get('sm20_date_from', date(2025, 1, 1))
    default_to = st.session_state.get('sm20_date_to', date.today())
    date_from = st.date_input("From", value=default_from)
    date_to = st.date_input("To", value=default_to)

# ─────────────────────────────────────────────
#  DATA PROCESSING (CACHED FOR SPEED)
# ─────────────────────────────────────────────
@st.cache_data(show_spinner="⚡ Reading files (Cached for speed!)...")
def process_files(u_file, a_file, s_files):
    # Reset file pointers just in case
    u_file.seek(0)
    a_file.seek(0)
    for f in s_files: f.seek(0)
    
    # 1. Read SAP User List
    user_df = strip_cols(read_file(u_file))
    u_cols = user_df.columns
    
    col_uid = _pick(u_cols, ["SAP ID", "User ID", "Users", "User Name"], 0)
    col_uname = _pick(u_cols, ["Complete name", "Full Name", "Username", "Name"], 1)
    col_dept = _pick(u_cols, ["Department", "Dept", "Division"], 2)
    col_mgr = _pick(u_cols, ["Reporting Manager", "Manager", "Supervisor"], None)
    col_created = _pick(u_cols, ["User Created On", "Created On", "Creation Date", "Valid from", "Date"], None)
    col_type = _pick(u_cols, ["User Type Text", "Technical User Type", "User Type", "Type"], None)
    col_valid_from = _pick(u_cols, ["Valid from", "Valid From Date"], None)
    col_valid_to = _pick(u_cols, ["Valid to", "Valid To Date"], None)
    
    user_clean = pd.DataFrame()
    user_clean['SAP ID'] = normalise_id(user_df[col_uid]) if col_uid else "UNKNOWN"
    user_clean['Username'] = user_df[col_uname] if col_uname else "UNKNOWN"
    user_clean['Department'] = user_df[col_dept].fillna("N/A") if col_dept else "N/A"
    user_clean['Reporting Manager'] = user_df[col_mgr] if col_mgr else "N/A"
    user_clean['User Created On'] = pd.to_datetime(user_df[col_created], errors='coerce').dt.strftime('%d/%m/%Y').fillna('N/A') if col_created else "N/A"
    user_clean['Valid from'] = pd.to_datetime(user_df[col_valid_from], errors='coerce').dt.strftime('%d/%m/%Y').fillna('N/A') if col_valid_from else "N/A"
    user_clean['Valid to'] = pd.to_datetime(user_df[col_valid_to], errors='coerce').dt.strftime('%d/%m/%Y').fillna('N/A') if col_valid_to else "N/A"
    
    filtered_msg = None
    # Filter for Dialog Users
    if col_type:
        original_len = len(user_clean)
        mask = user_df[col_type].astype(str).str.strip().str.upper().str.contains('DIALOG')
        user_clean = user_clean[mask]
        if len(user_clean) < original_len:
            filtered_msg = f"Filtered {original_len - len(user_clean)} non-Dialog users. Remaining Dialog users: {len(user_clean)}"
    else:
        filtered_msg = "⚠️ 'User Type' column not found in User List. Proceeding without Dialog filter."
        
    # 2. Read Access List
    acc_df = strip_cols(read_file(a_file))
    a_cols = acc_df.columns
    
    col_acc_id = _pick(a_cols, ["SAP ID", "User ID", "Users", "Username"], 0)
    col_acc_tcode = _pick(a_cols, ["Tcode", "Transaction Code", "TCode", "Trans Code"], 1)
    
    acc_df['SAP_ID_Norm'] = normalise_id(acc_df[col_acc_id])
    acc_df['Tcode_Norm'] = acc_df[col_acc_tcode].astype(str).str.strip().str.upper()
    
    # Extract Reporting Manager from Access List if present
    col_acc_mgr = _pick(a_cols, ["Reporting Manager", "Manager", "Supervisor"], None)
    if col_acc_mgr and (user_clean['Reporting Manager'] == "N/A").all():
        mgr_map = acc_df.drop_duplicates('SAP_ID_Norm').set_index('SAP_ID_Norm')[col_acc_mgr].to_dict()
        user_clean['Reporting Manager'] = user_clean['SAP ID'].map(mgr_map).fillna("N/A")
    
    # Count assigned Tcodes
    assigned_counts = acc_df.groupby('SAP_ID_Norm')['Tcode_Norm'].nunique().reset_index()
    assigned_counts.columns = ['SAP ID', 'Tcodes Assigned to user (Nos)']
    
    # 3. Read & Merge SM20 Logs
    sm20_dfs = []
    logon_dfs = []   # ← NEW: separate list for "Logon successful" rows only
    for f in s_files:
        sdf = strip_cols(read_file(f))
        s_cols = sdf.columns
        c_s_id   = _pick(s_cols, ["User Name", "Usr Nam", "User", "SAP ID"], 0)
        c_s_date = _pick(s_cols, ["Creation Date", "Date", "Log Date"], 1)
        c_s_time = _pick(s_cols, ["Creation time of audit entry", "Time", "Log Time", "Creation time"], None)
        c_s_msg  = _pick(s_cols, ["Audit Log Msg. Text", "Audit Log Msg Text", "Message Text", "Msg Text"], None)
        c_s_var  = _pick(s_cols, ["Variable Message Data", "Var Message Data", "Variable Data"], None)
        
        # ── Shared base columns ──────────────────────────────────────────────
        sap_id_series = normalise_id(sdf[c_s_id])
        unique_dates  = sdf[c_s_date].dropna().unique()
        date_map      = pd.Series(pd.to_datetime(unique_dates, errors='coerce'), index=unique_dates)
        log_date_series = sdf[c_s_date].map(date_map)
        log_time_series = (
            sdf[c_s_time].astype(str).str.strip()
            if (c_s_time and c_s_time in sdf.columns)
            else pd.Series(["N/A"] * len(sdf), index=sdf.index)
        )

        # ── A) Capture "Logon successful" rows (NEW – for Login Count) ───────
        if c_s_msg and c_s_msg in sdf.columns:
            msg_series  = sdf[c_s_msg].astype(str).str.strip()
            logon_mask  = msg_series.str.lower().str.contains("logon successful", na=False)
            logon_chunk = pd.DataFrame({
                'SAP ID':   sap_id_series[logon_mask].values,
                'Log Date': log_date_series[logon_mask].values,
                'Log Time': log_time_series[logon_mask].values,
                'Audit Log Msg. Text': msg_series[logon_mask].values,
            })
            logon_dfs.append(logon_chunk)

        # ── B) Capture transaction rows (existing logic, unchanged) ──────────
        clean_s = pd.DataFrame()
        clean_s['SAP ID']   = sap_id_series
        clean_s['Log Date'] = log_date_series
        clean_s['Log Time'] = log_time_series
        
        # New Logic (based on actual SM20 data format):
        # "Audit Log Msg. Text" contains entries like "Transaction FBL1N started." (note the dot)
        # "Variable Message Data" contains the actual Tcode (e.g. FBL1N, SA38, FB03)
        # Steps:
        #   1. Filter rows where msg starts with "Transaction" AND ends with "started." (with dot)
        #   2. Read Tcode from "Variable Message Data" column
        #   3. Exclude SESSION_MANAGER and SEARCH_SAP-MENU from Variable Message Data
        if c_s_msg and c_s_msg in sdf.columns:
            msg_series = sdf[c_s_msg].astype(str).str.strip()
            msg_lower = msg_series.str.lower()
            # Key fix: messages end with "started." (with a period/dot at the end)
            mask_msg = (
                msg_lower.str.startswith("transaction") &
                (msg_lower.str.endswith("started.") | msg_lower.str.endswith("started"))
            )
            clean_s = clean_s[mask_msg].copy()

            # The actual Tcode is in Variable Message Data
            if c_s_var and c_s_var in sdf.columns:
                var_series = sdf[c_s_var].astype(str).str.strip()
                var_filtered = var_series[mask_msg]

                # Exclude SESSION_MANAGER and SEARCH_SAP-MENU / SEARCH_SAP_MENU
                EXCLUDED_VAR = ["SESSION_MANAGER", "SEARCH_SAP-MENU", "SEARCH_SAP_MENU"]
                var_mask = ~var_filtered.str.upper().isin(EXCLUDED_VAR)

                # Tcode = Variable Message Data value (cleaned + uppercased)
                tcode_series = var_filtered.str.strip().str.upper()
                tcode_series = tcode_series.replace(["NAN", "NONE", "NAT", "", "<NAN>", "<NA>"], pd.NA)
                clean_s['Tcode'] = tcode_series.values
                clean_s = clean_s[var_mask.values].copy()
            else:
                # Fallback: extract Tcode from between "Transaction " and " started"
                msg_filtered = msg_series[mask_msg]
                extracted = msg_filtered.str.extract(r'(?i)^transaction\s+(\S+)\s+started')[0]
                extracted = extracted.str.strip().str.upper()
                extracted = extracted.replace(["NAN", "NONE", "NAT", "", "<NAN>", "<NA>"], pd.NA)
                clean_s['Tcode'] = extracted.values
                # Still exclude SESSION_MANAGER/SEARCH_SAP-MENU
                EXCL = {"SESSION_MANAGER", "SEARCH_SAP-MENU"}
                clean_s = clean_s[~clean_s['Tcode'].isin(EXCL)]
        else:
            # Final fallback: use Triggering Transaction Code column (old logic)
            c_s_tcode = _pick(s_cols, ["Triggering Transaction Code", "Tcode", "Transaction Code"], 2)
            if c_s_tcode and c_s_tcode in sdf.columns:
                t_series = sdf[c_s_tcode].astype(str).str.strip().str.upper()
                t_series = t_series.replace(["NAN", "NONE", "NAT", "", "<NAN>", "<NA>"], pd.NA)
                clean_s['Tcode'] = t_series
                EXCLUDED_TCODES = {"S000", "SESSION_MANAGER"}
                clean_s = clean_s[
                    clean_s['Tcode'].notna() &
                    ~clean_s['Tcode'].isin(EXCLUDED_TCODES)
                ]
            else:
                clean_s['Tcode'] = pd.NA
        
        sm20_dfs.append(clean_s)

    sm20_all = pd.concat(sm20_dfs, ignore_index=True)
    sm20_all = sm20_all.dropna(subset=['Log Date'])
    
    # Remove rows with no extracted Tcode
    sm20_all = sm20_all[sm20_all['Tcode'].notna()]

    # ── Consolidate logon-successful rows ────────────────────────────────────
    if logon_dfs:
        logon_all = pd.concat(logon_dfs, ignore_index=True)
        logon_all = logon_all.dropna(subset=['Log Date'])
    else:
        logon_all = pd.DataFrame(columns=['SAP ID', 'Log Date', 'Log Time', 'Audit Log Msg. Text'])
    
    # Keep a clean copy of acc_df for raw preview (without internal _Norm columns)
    acc_df_raw = acc_df.drop(columns=['SAP_ID_Norm', 'Tcode_Norm'], errors='ignore')
    
    return user_clean, acc_df_raw, sm20_all, assigned_counts, filtered_msg, logon_all

def generate_report(user_clean, assigned_counts, sm20_all, logon_all, d_from, d_to):
    # Filter SM20 (transactions) by Date Range
    sm20_filtered = sm20_all[(sm20_all['Log Date'].dt.date >= d_from) & (sm20_all['Log Date'].dt.date <= d_to)]

    # ── Login Count: count only "Logon successful" events ────────────────────
    logon_filtered = logon_all[
        (logon_all['Log Date'].dt.date >= d_from) &
        (logon_all['Log Date'].dt.date <= d_to)
    ]
    logon_agg = logon_filtered.groupby('SAP ID').agg(
        Login_count=('Log Date', 'count'),
        Last_logon=('Log Date', 'max')
    ).reset_index()

    # ── Transaction aggregations: unique Tcodes used & last transaction date ─
    txn_agg = sm20_filtered.groupby('SAP ID').agg(
        Tcodes_used=('Tcode', 'nunique'),
        Last_txn=('Log Date', 'max')
    ).reset_index()

    # Merge logon + transaction aggregations
    sm20_agg = pd.merge(logon_agg, txn_agg, on='SAP ID', how='outer')
    # Last Login Date = latest of logon or transaction date
    sm20_agg['Last_login'] = sm20_agg[['Last_logon', 'Last_txn']].max(axis=1)
    sm20_agg['Login_count'] = sm20_agg['Login_count'].fillna(0).astype(int)
    sm20_agg['Tcodes_used'] = sm20_agg['Tcodes_used'].fillna(0).astype(int)
    
    # Calculate dynamic months
    delta = relativedelta(d_to, d_from)
    months = delta.years * 12 + delta.months
    if delta.days > 0: months += 1
    if months == 0: months = 1
    
    col_login = f"Login count in {months} months (Nos)"
    col_used = f"Tcode Used in Last {months} months (Nos)"
    
    sm20_agg.rename(columns={
        'Login_count': col_login,
        'Tcodes_used': col_used,
        'Last_login': 'Last Login Date'
    }, inplace=True)
    
    # 4. Merge Everything
    final_df = pd.merge(user_clean, assigned_counts, on='SAP ID', how='left')
    final_df = pd.merge(final_df, sm20_agg, on='SAP ID', how='left')
    
    # Fill NAs
    final_df['Tcodes Assigned to user (Nos)'] = final_df['Tcodes Assigned to user (Nos)'].fillna(0).astype(int)
    final_df[col_login] = final_df[col_login].fillna(0).astype(int)
    final_df[col_used] = final_df[col_used].fillna(0).astype(int)
    
    # Calculate extra metrics
    final_df['Last Login Date Raw'] = final_df['Last Login Date']
    final_df['Last Login Date'] = final_df['Last Login Date'].dt.strftime('%d/%m/%Y').fillna('Never')
    
    today_ts = pd.Timestamp(d_to)
    days_inactive = (today_ts - final_df['Last Login Date Raw']).dt.days
    
    # Format Aging of non Usage as clean integers, avoiding float representations
    final_df['Aging of non Usage'] = [str(int(x)) if pd.notna(x) else "N/A" for x in days_inactive]
    
    util = (final_df[col_used] / final_df['Tcodes Assigned to user (Nos)']) * 100
    final_df['Tcode utilization in %'] = util.fillna(0).replace([float('inf'), float('-inf')], 0).round(0).clip(upper=100).astype(int)
    
    final_df.insert(0, 'SL. No.', range(1, len(final_df) + 1))
    
    # Conditionally add Valid to if present
    display_cols = [
        'SL. No.', 'SAP ID', 'Username', 'Department', 'Reporting Manager', 'User Created On'
    ]
    if 'Valid to' in user_clean.columns:
        display_cols.append('Valid to')
        
    display_cols.extend([
        col_login, 'Tcodes Assigned to user (Nos)', col_used,
        'Last Login Date', 'Aging of non Usage', 'Tcode utilization in %'
    ])
    
    master_table = final_df[display_cols].copy()
    
    return master_table, display_cols

files_ready = user_file and access_file and sm20_files

if files_ready:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("▶ Run Analysis", type="primary", use_container_width=True):
            st.session_state['analysis_run'] = True
            
            # Run and store RAW data in session state
            ud, ad, sa, ac, fm, lo = process_files(user_file, access_file, sm20_files)
            st.session_state['sap_data'] = {
                'user_clean': ud, 'acc_df': ad, 'sm20_all': sa, 'assigned_counts': ac,
                'filtered_msg': fm, 'logon_all': lo
            }
            
            # Auto-detect SM20 date range and set as defaults
            sm20_min = sa['Log Date'].min()
            sm20_max = sa['Log Date'].max()
            if pd.notna(sm20_min) and pd.notna(sm20_max):
                st.session_state['sm20_date_from'] = sm20_min.date()
                st.session_state['sm20_date_to'] = sm20_max.date()
            
            st.rerun()
            
    st.markdown("<hr>", unsafe_allow_html=True)
            
if not st.session_state.get('analysis_run', False) or 'sap_data' not in st.session_state:
    if files_ready:
        st.info("👆 Click the **Run Analysis** button above to generate the report based on your uploaded files.")
    else:
        st.info("ℹ️ Please upload the **SAP User List**, **User Access List**, and at least one **SM20 Audit Log** in the sidebar to generate the summary table.")
    st.stop()
    
# Load RAW data from session state
sap_data = st.session_state['sap_data']
user_clean = sap_data['user_clean']
user_df = sap_data['user_clean']  # For raw preview compatibility
acc_df = sap_data['acc_df']
sm20_all = sap_data['sm20_all']
assigned_counts = sap_data['assigned_counts']
filtered_msg = sap_data['filtered_msg']
logon_all = sap_data.get('logon_all', pd.DataFrame(columns=['SAP ID', 'Log Date', 'Log Time', 'Audit Log Msg. Text']))

# DYNAMICALLY generate report based on current date selection!
master_table, display_cols = generate_report(user_clean, assigned_counts, sm20_all, logon_all, date_from, date_to)

if filtered_msg:
    if "⚠️" in filtered_msg:
        st.info(filtered_msg)
    else:
        st.success(filtered_msg)
        

# ─────────────────────────────────────────────
#  UI: RAW DATA PREVIEW
# ─────────────────────────────────────────────
st.markdown("### 🔍 Raw Data Previews")
p1, p2, p3 = st.tabs(["👥 SAP User List", "🗂️ User Access List", "📋 SM20 Audit Logs (Merged)"])
with p1:
    st.caption(f"Rows: **{len(user_df):,}** | Columns: **{len(user_df.columns)}**")
    st.dataframe(user_df, use_container_width=True, hide_index=True, height=300)
with p2:
    st.caption(f"Rows: **{len(acc_df):,}** | Columns: **{len(acc_df.columns)}**")
    st.dataframe(acc_df, use_container_width=True, hide_index=True, height=300)
with p3:
    st.caption(f"Rows: **{len(sm20_all):,}** | Columns: **{len(sm20_all.columns)}**")
    st.dataframe(sm20_all, use_container_width=True, hide_index=True, height=300)
        
st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  UI: DEPARTMENT FILTER & TABLE DISPLAY
# ─────────────────────────────────────────────
st.markdown("### 📊 Summary Table")

# Color Legend Indicator
st.info("""
💡 **Tcode Utilization Legend:**
*   🟢 **Green Progress Bar (>= 50%):** Good utilization.
*   🟡 **Yellow Progress Bar (1% to 49%):** Low utilization.
*   🔴 **Red Highlight (0%):** No utilization (inactive).
""")


# Department filter
all_depts = ["All Departments"] + sorted([str(d) for d in master_table['Department'].unique() if pd.notna(d)])
selected_dept = st.selectbox("🏢 Filter by Department:", all_depts, key="dept_filter_select")

if selected_dept != "All Departments":
    filtered_table = master_table[master_table['Department'] == selected_dept].copy()
else:
    filtered_table = master_table.copy()

# User-wise search (below department filter)
user_search = st.text_input("🔍 Search by User (SAP ID or Username):", "", key="summary_user_search",
    placeholder="Type SAP ID or username to filter...")
if user_search.strip():
    mask = (
        filtered_table['SAP ID'].astype(str).str.contains(user_search.strip(), case=False, na=False) |
        filtered_table['Username'].astype(str).str.contains(user_search.strip(), case=False, na=False)
    )
    filtered_table = filtered_table[mask].copy()

# Re-index SL. No. after filter
filtered_table['SL. No.'] = range(1, len(filtered_table) + 1)



# Show result count banner
if user_search.strip():
    if len(filtered_table) == 0:
        st.warning(f"⚠️ No users found matching **'{user_search}'** in the selected department.")
    else:
        st.success(f"✨ Showing **{len(filtered_table):,}** user(s) matching **'{user_search}'**"
                   + (f" in **{selected_dept}**" if selected_dept != 'All Departments' else '') + ".")
elif selected_dept != "All Departments":
    st.info(f"🏢 Showing **{len(filtered_table):,}** user(s) in **{selected_dept}**.")
else:
    st.info(f"📊 Showing all **{len(filtered_table):,}** users.")

# Prepare CSV for download buttons
csv = filtered_table.to_csv(index=False).encode('utf-8')

# ── Build column config for native st.dataframe() ────────────────────────────
# Detect dynamic column names
util_col  = "Tcode utilization in %"
login_col = [c for c in filtered_table.columns if c.startswith("Login count")][0]
used_col  = [c for c in filtered_table.columns if c.startswith("Tcode Used")][0]

col_cfg = {
    "SL. No.":                          st.column_config.NumberColumn("SL. No.",                      width="small"),
    "SAP ID":                           st.column_config.TextColumn("SAP ID"),
    "Username":                         st.column_config.TextColumn("Username"),
    "Department":                       st.column_config.TextColumn("Department"),
    "Reporting Manager":                st.column_config.TextColumn("Reporting Manager"),
    "User Created On":                  st.column_config.TextColumn("User Created On"),
    "Valid to":                         st.column_config.TextColumn("Valid to"),
    login_col:                          st.column_config.NumberColumn(login_col),
    "Tcodes Assigned to user (Nos)":    st.column_config.NumberColumn("Tcodes Assigned to user (Nos)"),
    used_col:                           st.column_config.NumberColumn(used_col),
    "Last Login Date":                  st.column_config.TextColumn("Last Login Date"),
    "Aging of non Usage":               st.column_config.TextColumn("Aging of non Usage"),
    # util_col rendered via Styler below — no ProgressColumn here
}

# ── Pandas Styler: conditional color on Tcode utilization % ──────────────────
# Rule: 0% -> Red cell | 1-49% -> Yellow cell | >=50% -> Green cell
def _color_util_col(col):
    styles = []
    for val in col:
        try:
            pct = int(val)
        except (ValueError, TypeError):
            pct = 0
        if pct == 0:
            styles.append("background-color: #fdecea; color: #b71c1c; font-weight: 700;")
        elif pct < 50:
            styles.append("background-color: #fff8e1; color: #e65100; font-weight: 700;")
        else:
            styles.append("background-color: #e8f5e9; color: #1b5e20; font-weight: 700;")
    return styles

styled_table = filtered_table.style.apply(_color_util_col, subset=[util_col])

# Display as native Streamlit dataframe (same style as Detailed Audit Log)
st.dataframe(
    styled_table,
    use_container_width=True,
    hide_index=True,
    height=600,
    column_config=col_cfg,
)

# Download Button below the table
st.markdown("<br>", unsafe_allow_html=True)
st.download_button(
    label="⬇️ Download Summary Table (CSV)",
    data=csv,
    file_name=f"SAP_Usage_Summary_{selected_dept.replace(' ', '_')}.csv",
    mime="text/csv",
    key="download_summary_full"
)

# ─────────────────────────────────────────────
#  UI: DETAILED TRANSACTION & LOGIN LOGS
# ─────────────────────────────────────────────
st.markdown("<hr style='margin: 40px 0;'>", unsafe_allow_html=True)
st.markdown("### 📋 Detailed SAP Login & Transaction Audit Log")

users_info = user_clean[['SAP ID', 'Username', 'Department']].copy()

# ── A) Logon Successful events (used for Login Count) ───────────────────────
logon_filtered = logon_all[
    (logon_all['Log Date'].dt.date >= date_from) &
    (logon_all['Log Date'].dt.date <= date_to)
].copy()
logon_detail = pd.merge(logon_filtered, users_info, on='SAP ID', how='inner')
if selected_dept != "All Departments":
    logon_detail = logon_detail[logon_detail['Department'] == selected_dept].copy()
logon_detail['Event Type']     = 'Logon'
logon_detail['For which Tcode'] = '—'
logon_detail['Login Date']     = logon_detail['Log Date'].dt.strftime('%d/%m/%Y')
logon_detail['Login Time']     = logon_detail['Log Time'].fillna('00:00:00').astype(str).str.strip().replace(
    ['nan', 'NAN', 'NaN', 'None', 'NaT', 'N/A', ''], '00:00:00'
)
logon_detail['Audit Log Msg. Text'] = logon_detail['Audit Log Msg. Text'].astype(str)

# ── B) Transaction events ────────────────────────────────────────────────────
sm20_filtered = sm20_all[
    (sm20_all['Log Date'].dt.date >= date_from) &
    (sm20_all['Log Date'].dt.date <= date_to)
].copy()
txn_detail = pd.merge(sm20_filtered, users_info, on='SAP ID', how='inner')
if selected_dept != "All Departments":
    txn_detail = txn_detail[txn_detail['Department'] == selected_dept].copy()
txn_detail = txn_detail[txn_detail['Tcode'].notna()].copy()
txn_detail['Event Type']           = 'Transaction'
txn_detail['For which Tcode']      = txn_detail['Tcode']
txn_detail['Login Date']           = txn_detail['Log Date'].dt.strftime('%d/%m/%Y')
txn_detail['Login Time']           = txn_detail['Log Time'].fillna('00:00:00').astype(str).str.strip().replace(
    ['nan', 'NAN', 'NaN', 'None', 'NaT', 'N/A', ''], '00:00:00'
)
txn_detail['Audit Log Msg. Text']  = '—'

# ── C) Combine & sort descending by datetime ─────────────────────────────────
combined_cols = ['SAP ID', 'Username', 'Login Date', 'Login Time', 'Log Date',
                 'Event Type', 'For which Tcode', 'Audit Log Msg. Text']
detailed_logs = pd.concat(
    [logon_detail[combined_cols], txn_detail[combined_cols]],
    ignore_index=True
)
detailed_logs['Datetime'] = pd.to_datetime(
    detailed_logs['Log Date'].dt.strftime('%Y-%m-%d') + ' ' + detailed_logs['Login Time'],
    errors='coerce'
)
detailed_logs = detailed_logs.sort_values(by='Datetime', ascending=False)

# ── Display columns ──────────────────────────────────────────────────────────
display_detailed = detailed_logs[[
    'SAP ID', 'Username', 'Login Date', 'Login Time',
    'Event Type', 'For which Tcode', 'Audit Log Msg. Text'
]].copy()

# Add search input for user ID or Name
log_search = st.text_input("🔍 Search Audit Log by User (SAP ID or Username):", "", key="detailed_log_user_search")
if log_search:
    display_detailed = display_detailed[
        display_detailed['SAP ID'].str.contains(log_search, case=False, na=False) |
        display_detailed['Username'].str.contains(log_search, case=False, na=False)
    ].copy()

# Add SL. No.
display_detailed.insert(0, 'SL. No.', range(1, len(display_detailed) + 1))

# Show a count banner
total_logons = len(display_detailed[display_detailed['Event Type'] == 'Logon'])
total_txns   = len(display_detailed[display_detailed['Event Type'] == 'Transaction'])
total_matching = len(display_detailed)
st.info(
    f"✨ Found **{total_matching:,}** total entries — "
    f"🔑 **{total_logons:,}** Logon Successful events & "
    f"📂 **{total_txns:,}** Transaction events — "
    f"in the selected date range & department."
)

# Column config for the detailed log
detailed_col_cfg = {
    'SL. No.':              st.column_config.NumberColumn('SL. No.', width='small'),
    'SAP ID':               st.column_config.TextColumn('SAP ID'),
    'Username':             st.column_config.TextColumn('Username'),
    'Login Date':           st.column_config.TextColumn('Login Date'),
    'Login Time':           st.column_config.TextColumn('Login Time'),
    'Event Type':           st.column_config.TextColumn('Event Type', width='small'),
    'For which Tcode':      st.column_config.TextColumn('For which Tcode'),
    'Audit Log Msg. Text':  st.column_config.TextColumn('Audit Log Msg. Text'),
}

# Display full detailed logs without row limit
st.dataframe(display_detailed, use_container_width=True, hide_index=True, height=600,
             column_config=detailed_col_cfg)

# Download Button for the filtered logs
if total_matching > 0:
    detailed_csv = display_detailed.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download Detailed Audit Log (CSV)",
        data=detailed_csv,
        file_name=f"Detailed_SAP_Audit_Log_{selected_dept.replace(' ', '_')}.csv",
        mime="text/csv",
        key="download_detailed_audit_logs"
    )