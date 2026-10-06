import streamlit as st
import pandas as pd
from dateutil.relativedelta import relativedelta
from utils import ui_helpers

st.set_page_config(page_title="Functional Wise SAP Analysis", page_icon="datasets/Hero_Section_Imgaes/logo.png", layout="wide")
st.logo("datasets/Hero_Section_Imgaes/logo.png")
ui_helpers.inject_custom_css()
ui_helpers.inject_top_right_logo()
st.title("📊 Functional Wise SAP Analysis")

if 'sap_data' not in st.session_state:
    st.warning("Please go to 'SAP Usage Analysis' page to upload and run analysis first.")
    st.stop()

sap_data = st.session_state['sap_data']
access_df = sap_data['acc_df'].copy()
users_df = sap_data['user_clean'].copy()
sm20_df = sap_data['sm20_all'].copy() if 'sm20_all' in sap_data else None

# Auto-detect key columns from actual data
def pick_col(cols, candidates, fallback_idx=0):
    for c in candidates:
        if c in cols:
            return c
    return cols[fallback_idx]

user_cols = list(users_df.columns)
acc_cols  = list(access_df.columns)

c_aid  = pick_col(acc_cols,  ["SAP ID", "User ID", "Users", "Username"])
c_uid  = pick_col(user_cols, ["Users", "SAP ID", "User ID", "Username"])
c_uname = pick_col(user_cols, ["Complete name", "Full Name", "Name", "Username"], fallback_idx=1)
dept_col = pick_col(user_cols, ["Department", "Dept", "DEPT", "department"])

tcode_col = "Tcode" if "Tcode" in access_df.columns else access_df.columns[-1]
desc_col = "Tcode Description" if "Tcode Description" in access_df.columns else None

# Helper: pick the right SM20 column by known names
def pick_sm20_col(cols, candidates):
    for c in candidates:
        if c in cols:
            return c
    return None

# Helper to merge usernames safely
def get_access_with_names():
    df = access_df.copy()
    if c_uname in df.columns:
        df = df.drop(columns=[c_uname])
    if dept_col and dept_col in df.columns and dept_col != c_aid:
        df = df.drop(columns=[dept_col])
    df[c_aid] = df[c_aid].astype(str).str.strip()
    
    cols_to_select = [c_uid, c_uname]
    if dept_col and dept_col in users_df.columns:
        cols_to_select.append(dept_col)
        
    users_temp = users_df[cols_to_select].drop_duplicates(subset=[c_uid]).copy()
    users_temp[c_uid] = users_temp[c_uid].astype(str).str.strip()
    df = df.merge(users_temp, left_on=c_aid, right_on=c_uid, how="left")
    df[c_uname] = df[c_uname].fillna(df[c_aid])
    return df.reset_index(drop=True)

# Helper to format grouped dataframe
def make_grouped_df(df, group_cols, detail_cols, value_col=None, show_subtotal=False, subtotal_label_col=None, subtotal_sum=False):
    df = df.reset_index(drop=True).sort_values(by=group_cols + detail_cols)
    formatted = []
    is_single_group = len(group_cols) == 1

    for name, group in df.groupby(group_cols, sort=False, dropna=False):
        first = True
        for _, row in group.iterrows():
            record = {}
            for i, gc in enumerate(group_cols):
                val = name if is_single_group else name[i]
                record[gc] = val if first else ""
            for dc in detail_cols:
                record[dc] = row[dc]
            if value_col:
                record[value_col] = row[value_col]
            formatted.append(record)
            first = False

        # ── Subtotal row per group ──────────────────────────────
        if show_subtotal:
            subtotal_record = {gc: "" for gc in group_cols}
            for dc in detail_cols:
                subtotal_record[dc] = ""

            # Build label like "Rabindra Nath Sinha Total"
            if subtotal_label_col and subtotal_label_col in group_cols:
                idx = group_cols.index(subtotal_label_col)
                label_val = name if is_single_group else name[idx]
            else:
                label_val = name if is_single_group else " ".join(str(n) for n in name)

            # Put label in first detail col
            if detail_cols:
                subtotal_record[detail_cols[0]] = f"{label_val} Total"

            # Total value: sum of value_col (for real counts) or row count
            if value_col:
                if subtotal_sum and value_col in group.columns:
                    subtotal_record[value_col] = int(group[value_col].sum())
                else:
                    subtotal_record[value_col] = len(group)

            subtotal_record["__is_total__"] = True
            formatted.append(subtotal_record)

    result = pd.DataFrame(formatted)
    if "__is_total__" in result.columns:
        result = result.drop(columns=["__is_total__"])
    return result


access_with_names = get_access_with_names()

# -------------------------------------------------------------------------
# Department Filter (Applies to all sections)
# -------------------------------------------------------------------------
if dept_col and dept_col in users_df.columns:
    all_depts = ["All Departments"] + sorted([str(d) for d in users_df[dept_col].dropna().unique() if str(d).strip() != ""])
    selected_dept = st.selectbox("Filter by Department (All Sections):", all_depts)
else:
    selected_dept = "All Departments"

# Filter access data by department
if selected_dept != "All Departments" and dept_col and dept_col in access_with_names.columns:
    access_with_names_filtered = access_with_names[access_with_names[dept_col] == selected_dept].copy()
else:
    access_with_names_filtered = access_with_names.copy()

# Build Tcode -> Description mapping
tcode_desc_map = {}
if desc_col:
    tcode_desc_map = (
        access_df.drop_duplicates(subset=[tcode_col])
        .set_index(tcode_col)[desc_col]
        .to_dict()
    )

# -------------------------------------------------------------------------
# UI Layout
# -------------------------------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "1. Tcodes Assigned to Users",
    "2. Same Transaction Assigned to users",
    "3. Tcode Usage by Tcode",
    "4. Tcode Usage by User"
])

with tab1:
    st.subheader("Tcodes Assigned to Users")
    if tcode_col in access_df.columns and c_aid in access_df.columns:
        df1 = access_with_names_filtered.drop_duplicates(subset=[c_aid, tcode_col]).reset_index(drop=True)
        df1_clean = pd.DataFrame({
            "SAP ID": df1[c_aid].values,
            "Username": df1[c_uname].values,
            "Tcode": df1[tcode_col].values
        })
        if desc_col:
            df1_clean["Tcode Description"] = df1[desc_col].values
        df1_clean["Total"] = 1

        group_cols = ["SAP ID", "Username"]
        detail_cols = ["Tcode", "Tcode Description"] if desc_col else ["Tcode"]
        res1 = make_grouped_df(
            df1_clean, group_cols, detail_cols, "Total",
            show_subtotal=True, subtotal_label_col="Username"
        )
        st.dataframe(res1, use_container_width=True, hide_index=True)
        
        # ── Single User Search Section ─────────────────────────────────────
        st.markdown("<hr style='margin: 30px 0;'>", unsafe_allow_html=True)
        st.subheader("🔍 Search Specific User's Assigned Tcodes")
        
        # Build user selection list (SAP ID - Username)
        user_list = sorted(list(df1_clean.apply(lambda r: f"{r['SAP ID']} - {r['Username']}", axis=1).unique()))
        
        selected_user_lbl = st.selectbox(
            "Select User to view detailed Tcode assignments:",
            ["-- Select User --"] + user_list,
            key="tab1_user_search"
        )
        
        if selected_user_lbl != "-- Select User --":
            selected_sap_id = selected_user_lbl.split(" - ")[0]
            user_tcodes = df1_clean[df1_clean["SAP ID"] == selected_sap_id].copy()
            
            # Format and display
            user_tcodes_display = user_tcodes.drop(columns=["SAP ID", "Username", "Total"]).reset_index(drop=True)
            user_tcodes_display.insert(0, "SL. No.", range(1, len(user_tcodes_display) + 1))
            
            # Add a Total row at the bottom of the table
            total_count = len(user_tcodes_display)
            total_row = pd.DataFrame([{
                "SL. No.": "Total",
                "Tcode": f"{total_count} Assigned",
                "Tcode Description": ""
            }])
            user_tcodes_display = pd.concat([user_tcodes_display, total_row], ignore_index=True)
            
            st.success(f"📋 **{selected_user_lbl}** is assigned **{total_count}** transaction codes:")
            st.dataframe(user_tcodes_display, use_container_width=True, hide_index=True)
    else:
        st.info("Required columns not found.")

with tab2:
    st.subheader("Same Transaction Assigned to users")
    if tcode_col in access_df.columns and c_aid in access_df.columns:
        df2 = access_with_names_filtered.drop_duplicates(subset=[tcode_col, c_aid]).reset_index(drop=True)
        df2_clean = pd.DataFrame({
            "SAP ID": df2[c_aid].values,
            "Username": df2[c_uname].values,
            "Tcode": df2[tcode_col].values
        })
        if desc_col:
            df2_clean["Tcode Description"] = df2[desc_col].values
        df2_clean["Total"] = 1

        group_cols = ["Tcode", "Tcode Description"] if desc_col else ["Tcode"]
        detail_cols = ["SAP ID", "Username"]
        subtotal_lbl = "Tcode Description" if desc_col else "Tcode"
        res2 = make_grouped_df(
            df2_clean, group_cols, detail_cols, "Total",
            show_subtotal=True, subtotal_label_col=subtotal_lbl
        )
        st.dataframe(res2, use_container_width=True, hide_index=True)
    else:
        st.info("Required columns not found.")

if sm20_df is not None:
    sm20_cols = list(sm20_df.columns)

    # SM20 data is pre-processed: Tcode already extracted from "Audit Log Msg. Text"
    # and filtered by "Variable Message Data" in the SAP Usage Analysis page.
    # Use the fixed column names set during processing.
    c_suser = pick_sm20_col(sm20_cols, ["SAP ID", "User Name", "Usr Nam", "User", "Username"])
    c_stcode = pick_sm20_col(sm20_cols, ["Tcode"])

    if c_suser and c_stcode and c_suser in sm20_df.columns and c_stcode in sm20_df.columns:
        sm20_temp = sm20_df[[c_suser, c_stcode]].copy()
        sm20_temp[c_suser] = sm20_temp[c_suser].astype(str).str.strip()
        sm20_temp[c_stcode] = sm20_temp[c_stcode].astype(str).str.strip()

        # Remove system/batch users
        sm20_temp = sm20_temp[~sm20_temp[c_suser].str.upper().str.contains(
            "WF-BATCH|BATCH|SYSTEM|RFC|NAN|NONE", na=False)]
        # Remove purely numeric user IDs (system users)
        sm20_temp = sm20_temp[~sm20_temp[c_suser].str.match(r"^\d+$")]

        # Remove null/empty/NAN tcodes (already filtered at source, but safety check)
        invalid_tcodes = ["NAN", "NONE", "NA", "<NA>", "NAT", "", "SESSION_MANAGER", "SEARCH_SAP-MENU", "SEARCH_SAP_MENU"]
        sm20_temp = sm20_temp[~sm20_temp[c_stcode].str.upper().isin(invalid_tcodes)]

        # Merge with users to get Username & Department — inner join so only valid users appear
        cols_to_select = [c_uid, c_uname]
        if dept_col and dept_col in users_df.columns:
            cols_to_select.append(dept_col)
            
        users_temp = users_df[cols_to_select].drop_duplicates(subset=[c_uid]).copy()
        users_temp[c_uid] = users_temp[c_uid].astype(str).str.strip()

        sm20_with_names = sm20_temp.merge(users_temp, left_on=c_suser, right_on=c_uid, how="inner")

        # Calculate dynamic month label from SM20 data range
        _sm20_min = sm20_df['Log Date'].min() if 'Log Date' in sm20_df.columns else None
        _sm20_max = sm20_df['Log Date'].max() if 'Log Date' in sm20_df.columns else None
        if pd.notna(_sm20_min) and pd.notna(_sm20_max):
            _delta = relativedelta(_sm20_max, _sm20_min)
            _months = _delta.years * 12 + _delta.months
            if _delta.days > 0: _months += 1
            if _months == 0: _months = 1
        else:
            _months = 1
        tcode_used_label = f"Tcode Used in {_months} months"

        # Compute unfiltered usage for user-specific view (ignores department filter)
        usage_agg_all = (
            sm20_with_names.groupby([c_suser, c_uname, c_stcode], dropna=False)
            .size()
            .reset_index(name="Total")
        )
        usage_clean_all = pd.DataFrame({
            "SAP ID": usage_agg_all[c_suser].values,
            "Username": usage_agg_all[c_uname].values,
            tcode_used_label: usage_agg_all[c_stcode].values,
            "Total": usage_agg_all["Total"].values
        })
        if desc_col:
            usage_clean_all["Tcode Description"] = usage_clean_all[tcode_used_label].map(tcode_desc_map).fillna("")

        # Filter SM20 data by department
        if selected_dept != "All Departments" and dept_col and dept_col in sm20_with_names.columns:
            sm20_with_names = sm20_with_names[sm20_with_names[dept_col] == selected_dept].copy()

        # Group by user + tcode to get volume (Total)
        usage_agg = (
            sm20_with_names.groupby([c_suser, c_uname, c_stcode], dropna=False)
            .size()
            .reset_index(name="Total")
        )

        usage_clean = pd.DataFrame({
            "SAP ID": usage_agg[c_suser].values,
            "Username": usage_agg[c_uname].values,
            tcode_used_label: usage_agg[c_stcode].values,
            "Total": usage_agg["Total"].values
        })
        if desc_col:
            usage_clean["Tcode Description"] = usage_clean[tcode_used_label].map(tcode_desc_map).fillna("")

        with tab3:
            st.subheader("Volume of transactions performed (By Tcode)")
            group_cols3 = [tcode_used_label, "Tcode Description"] if desc_col else [tcode_used_label]
            detail_cols3 = ["SAP ID", "Username"]
            subtotal_lbl3 = "Tcode Description" if desc_col else tcode_used_label
            res3 = make_grouped_df(
                usage_clean, group_cols3, detail_cols3, "Total",
                show_subtotal=True, subtotal_label_col=subtotal_lbl3, subtotal_sum=True
            )
            st.dataframe(res3, use_container_width=True, hide_index=True)

        with tab4:
            st.subheader("Count of Transaction performed by users")
            group_cols4 = ["SAP ID", "Username"]
            detail_cols4 = [tcode_used_label, "Tcode Description"] if desc_col else [tcode_used_label]
            # Build the main table
            res4 = make_grouped_df(
                usage_clean, group_cols4, detail_cols4, "Total",
                show_subtotal=True, subtotal_label_col="Username", subtotal_sum=True
            )
            # Display full table first
            # ---- User specific search below ----
            user_search_tab4 = st.text_input("🔍 Search by SAP ID or Username", "", key="tab4_user_search")
            if user_search_tab4:
                # Filter the usage data (respecting department filter) before grouping
                filtered_usage = usage_clean[usage_clean["SAP ID"].str.contains(user_search_tab4, case=False, na=False) |
                                 usage_clean["Username"].str.contains(user_search_tab4, case=False, na=False)]
                filtered_res4 = make_grouped_df(
                    filtered_usage, group_cols4, detail_cols4, "Total",
                    show_subtotal=True, subtotal_label_col="Username", subtotal_sum=True
                )
                st.dataframe(filtered_res4, use_container_width=True, hide_index=True)
            else:
                # Show the full table when no search term
                st.dataframe(res4, use_container_width=True, hide_index=True)

    else:
        with tab3:
            st.warning(f"SM20 User column ('{c_suser}') or Tcode column ('{c_stcode}') not found in SM20 data.")
        with tab4:
            st.warning(f"SM20 User column ('{c_suser}') or Tcode column ('{c_stcode}') not found in SM20 data.")
else:
    with tab3:
        st.info("SM20 Audit Log not loaded. Upload it in the SAP Usage Analysis page.")
    with tab4:
        st.info("SM20 Audit Log not loaded. Upload it in the SAP Usage Analysis page.")
