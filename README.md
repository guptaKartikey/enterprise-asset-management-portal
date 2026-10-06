# 💻 Enterprise Asset & SAP Usage Analysis Portal

<p align="center">

### 🚀 [🌐 LIVE DEMO](https://enterprise-asset-management-app-hhrbodyqgfaxvhisxujul3.streamlit.app/)

</p>

<p align="center">

<img src="https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python" />
<img src="https://img.shields.io/badge/Streamlit-App-red?style=for-the-badge&logo=streamlit" />
<img src="https://img.shields.io/badge/Pandas-Data%20Analytics-purple?style=for-the-badge&logo=pandas" />
<img src="https://img.shields.io/badge/SAP-SM20%20Analytics-orange?style=for-the-badge&logo=sap" />
<img src="https://img.shields.io/badge/Status-Live-success?style=for-the-badge" />

</p>

---

## 🌐 Interactive Live Application

Experience the complete dashboard directly in your browser:

<p align="center">

<a href="https://enterprise-asset-management-app-hhrbodyqgfaxvhisxujul3.streamlit.app/">
<img src="https://img.shields.io/badge/🚀%20OPEN%20LIVE%20DASHBOARD-Streamlit-red?style=for-the-badge&logo=streamlit" />
</a>

</p>

> **Note:** The live application uses anonymized/mock data for demonstration and portfolio purposes.

---

## 📌 Overview

**Enterprise Asset & SAP Usage Analysis Portal** is an interactive enterprise analytics application built with **Python, Streamlit, and Pandas**.

The platform combines:

- 🖥️ IT Asset Lifecycle Management
- 👨‍💼 Employee Hardware Tracking
- 📊 SAP SM20 Security Audit Analytics
- 🔐 SAP T-Code Usage Analysis
- ⚠️ Terminal Login Violation Detection
- 📈 Interactive Enterprise Dashboards
- 📥 CSV Reporting & Data Export

The goal is to provide a centralized platform for analyzing **IT assets, employee allocations, SAP usage, transaction activity, and login anomalies**.

---

# 🧭 Dashboard Navigation

| Module | Description |
|---|---|
| 🏠 Enterprise Dashboard | Overall IT asset KPIs and analytics |
| 👤 Employee Search | Search employees and assigned hardware |
| 💻 Asset Management | Track assets and inventory |
| 📊 Asset Reports | Generate filtered asset reports |
| 🔐 SAP Usage Analysis | Analyze SAP SM20 audit activity |
| 🧩 Functional SAP Analysis | Compare assigned vs executed T-Codes |
| ⚠️ Login Violation Detection | Detect suspicious terminal access |

---

# 🌟 Key Features

## 🏢 1. Enterprise Asset Dashboard

Interactive dashboard for monitoring enterprise IT assets.

### KPIs

- 📦 Total Assets
- 💻 In-Use Devices
- 🏢 IT Stock / Spare Devices
- 👨‍💼 Employee Allocations

### Interactive Analysis

Users can analyze assets by:

- Department
- Location
- Asset Type
- Allocation Status

Supported asset categories include:

```text
Laptops
Desktops
Servers
Storage
IT Stock
```

---

## 👤 2. Advanced Employee Search

Search employees using multiple identifiers:

```text
Employee Name
Employee ID
Hardware Asset Tag
```

The employee profile provides:

- Employee information
- Department
- Assigned hardware
- Asset Tag
- Serial Number
- Warranty status
- Allocation details

---

## 💻 3. Asset & Inventory Management

Interactive filtering enables users to analyze enterprise hardware.

### Filters

```text
Department
Asset Type
Location
Allocation Status
```

### Reporting

Filtered results can be exported as:

```text
CSV
```

This makes the application useful for operational reporting and inventory audits.

---

# 🔐 4. SAP SM20 Usage & Audit Analysis

The portal provides interactive analytics for SAP Security Audit Logs (**SM20**).

### Capabilities

- Multi-month audit log analysis
- Transaction parsing
- Dialog user filtering
- Reporting manager mapping
- Department-wise analysis
- Login frequency analysis
- T-Code execution analysis
- User activity monitoring

---

# 🧩 5. Functional-Wise SAP Analysis

An interactive authorization matrix compares:

```text
Assigned T-Codes
        VS
Executed T-Codes
```

This helps identify:

- Assigned but unused T-Codes
- Executed transactions
- Functional usage patterns
- Department-wise activity

---

# ⚠️ 6. SAP Login Violation Detection

The application cross-verifies:

```text
Employee Hardware Allocation
              +
SAP Terminal Login Logs
              ↓
       Anomaly Detection
```

It can flag scenarios such as:

- 🚨 Login from an unassigned workstation
- 🚨 Unexpected terminal access
- 🚨 After-hours login activity
- 🚨 Potential credential-sharing indicators

> This module is designed as an analytics and anomaly-detection aid, not as a definitive security incident determination.

---

# 📊 Interactive Analytics

The dashboard supports interactive exploration through:

- 🔎 Search
- 🎛️ Filters
- 📈 Charts
- 📋 Data Tables
- 📊 KPI Cards
- 📥 CSV Export
- 🧩 Drill-down analysis

Users can change filters and immediately explore different subsets of the data.

---

# 📁 Sample / Mock Dataset

For public demonstration, the repository contains anonymized sample datasets:

```text
datasets/
└── Sample_Mock_Datasets/
    ├── mock_asset_data.csv
    ├── mock_asset_data.xlsx
    ├── mock_sap_users.xlsx
    ├── mock_sap_access.xlsx
    ├── mock_sm20_audit_log.xlsx
    └── mock_login_audit_report.xlsx
```

### Dataset Contents

| Dataset | Purpose |
|---|---|
| `mock_asset_data` | Employee assets and inventory |
| `mock_sap_users` | SAP user master data |
| `mock_sap_access` | SAP role & T-Code access |
| `mock_sm20_audit_log` | SAP SM20 activity logs |
| `mock_login_audit_report` | Terminal login anomaly cases |

---

# 🏗️ Application Architecture

```text
                 ┌─────────────────────┐
                 │     User / Admin    │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │  Streamlit Web App  │
                 └──────────┬──────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
       Asset Data       SAP SM20       SAP Access
             │              │              │
             └──────────────┼──────────────┘
                            ▼
                    ┌───────────────┐
                    │    Pandas     │
                    │ Data Processing│
                    └───────┬───────┘
                            │
                            ▼
                  ┌──────────────────┐
                  │ Interactive      │
                  │ Dashboards       │
                  └──────────────────┘
```

---

# 🛠️ Technology Stack

| Technology | Usage |
|---|---|
| 🐍 Python | Application & data processing |
| 🎈 Streamlit | Interactive web dashboard |
| 🐼 Pandas | Data processing & analysis |
| 📊 Data Visualization | Interactive analytics |
| 🔐 SAP SM20 | Security audit data |
| 📄 CSV / Excel | Data ingestion & reporting |

---

# 🚀 Quick Start

## 1️⃣ Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/enterprise-asset-management-portal.git
```

```bash
cd enterprise-asset-management-portal
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Run Application

```bash
streamlit run app.py
```

Or on Windows:

```text
start_app.bat
```

---

## 4️⃣ Open in Browser

```text
http://localhost:8501
```

---

# 🖥️ Recommended System

```text
Python 3.9+
4 GB RAM or higher
Modern Web Browser
Internet connection for live deployment
```

---

# 🔒 Privacy & Data Sanitization

This repository **does not contain real confidential enterprise data**.

For public demonstration:

- Employee names are anonymized
- Employee IDs are replaced
- Company names are replaced with generic identifiers
- Email addresses are removed
- Phone numbers are removed
- SAP audit records are mocked/anonymized
- Terminal information is sanitized

Example:

```text
Apex Enterprise
John Doe
EMP001
```

> ⚠️ Real employee information, SAP credentials, confidential logs, internal hostnames, IP addresses, or company-sensitive data should never be committed to a public repository.

---

# 📸 Screenshots

Add your dashboard screenshots here.

Example:

```markdown
<img width="1857" height="793" alt="image" src="https://github.com/user-attachments/assets/65b33ad3-4b6a-4883-ab3c-9d694e435385" />


<img width="1874" height="809" alt="image" src="https://github.com/user-attachments/assets/0bca440a-c73d-4f8b-9435-bfe89840c014" />

![Uploading image.png…]()

```

Recommended folder:

```text
assets/
└── screenshots/
    ├── enterprise-dashboard.png
    ├── employee-search.png
    ├── asset-management.png
    ├── sap-usage-dashboard.png
    └── login-violation-dashboard.png
```

---

# 🎯 Project Highlights

### 📦 Enterprise Asset Management

Centralized monitoring of employee hardware and IT inventory.

### 📊 SAP Analytics

Interactive analysis of SAP SM20 audit logs and transaction usage.

### 🔐 Security Analytics

Detection of potentially abnormal SAP terminal access.

### 📈 Data-Driven Reporting

Interactive filters, dashboards and CSV exports for operational analysis.

---

# 💡 Use Cases

This platform can support:

- IT Asset Audits
- Employee Hardware Tracking
- Inventory Monitoring
- SAP Usage Analysis
- T-Code Utilization Analysis
- Security Audit Analytics
- Terminal Access Monitoring
- Department-Level Reporting
- Operational Dashboards

---

# 🔮 Future Enhancements

Potential future improvements:

- 🤖 AI-powered anomaly detection
- 📧 Automated email reports
- 🗄️ PostgreSQL / MySQL integration
- 🔐 Role-based authentication
- 📊 Advanced BI dashboards
- 📅 Scheduled reports
- 🚨 Real-time security alerts
- ☁️ Enterprise cloud deployment

---

# 👨‍💻 Developer

### Kartikey Gupta

**B.Tech Computer Science & Engineering**

Interested in:

```text
Data Analytics
AI/ML
Python
Software Development
Business Intelligence
```

### 🔗 Connect

- 💼 [LinkedIn](https://www.linkedin.com/in/kartikey-gupta-988206372/)
- 🐙 [GitHub](https://github.com/)
- 🌐 [Portfolio](https://kartikey-gupta-portfolio.streamlit.app/)

---

# ⭐ Support the Project

If you find this project useful or interesting:

⭐ **Star this repository**

🍴 **Fork the repository**

💬 **Share your feedback**

---

<p align="center">

### 🚀 Built with Python + Streamlit + Pandas

**Enterprise Asset & SAP Usage Analysis Portal**

</p>

<p align="center">
© 2026 Kartikey Gupta
</p>
