# 💻 Enterprise Asset & SAP Usage Analysis Portal

A modern, high-performance web dashboard built with **Streamlit**, **Pandas**, and **Python** for comprehensive IT Asset Lifecycle Management, Employee Hardware Tracking, SAP Security Audit (SM20) Analytics, and Terminal Login Anomaly Detection.

---

## 🌟 Key Features

1. **Enterprise Asset Dashboard**
   - Live KPI cards tracking Total Assets, In-Use Devices, IT Stock (spares), and Employee allocations.
   - Interactive breakdown by Department, Location, and Asset Types (Laptops, Desktops, Servers, Storage).

2. **Advanced Employee Search & Profile**
   - Multi-criteria lookup by Employee Name, Employee ID, or Hardware Asset Tag.
   - Detailed Employee Profile Summary & assigned hardware specifications with serial numbers and warranty statuses.

3. **Asset & Inventory Reports**
   - Multi-facet filters by Department, Asset Type, and Location.
   - One-click export to clean CSV reports.

4. **SAP SM20 Usage & Audit Analysis**
   - Dynamic multi-month SM20 log ingestion and transaction parsing.
   - Dialog User filtering and reporting manager mapping.
   - Department-wise drill-downs, login frequency counts, and executed transaction analytics.

5. **Functional-Wise SAP Analysis**
   - Multi-tab authorization matrix tracking Assigned vs. Executed TCodes across enterprise functions.

6. **SAP Login Violation Detection**
   - Cross-verifies physical hardware allocations against SAP terminal connection logs.
   - Flags suspicious logins where users access SAP from unassigned workstations or after hours.

---

## 📁 Sample / Mock Datasets

A clean, anonymized sample dataset is included in `datasets/Sample_Mock_Datasets/` for demo and testing purposes:

- `mock_asset_data.csv` / `mock_asset_data.xlsx` (16 realistic asset rows with Laptops, Desktops, Servers, IT Stock)
- `mock_sap_users.xlsx` (Master SAP User List with Dialog and System users)
- `mock_sap_access.xlsx` (SAP Role and TCode access matrix)
- `mock_sm20_audit_log.xlsx` (Multi-month SM20 transaction and logon logs)
- `mock_login_audit_report.xlsx` (Terminal login records with violation test cases)

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.9+ installed

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
streamlit run app.py
```
Or double-click `start_app.bat` on Windows.

---

## 🛡️ Privacy & Sanitization Notice
All company names, employee personal details (names, emails, phone numbers), and confidential audit logs in this repository are replaced with generic identifiers (Apex Enterprise, John Doe, EMP001, etc.) to ensure privacy and compliance with public repository standards.
