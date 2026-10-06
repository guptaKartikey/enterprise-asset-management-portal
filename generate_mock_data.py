import os
import pandas as pd
import numpy as np

sample_dir = os.path.join(os.path.dirname(__file__), "datasets", "Sample_Mock_Datasets")
os.makedirs(sample_dir, exist_ok=True)

# 1. MOCK ASSET DATASET
asset_rows = [
    {
        'Asset Tag': 'APX-LAP-101', 'Asset Type': 'Laptop', 'Asset Category': 'Mobile Workstation', 'Asset State': 'In Use',
        'Connected or Isolated': 'Connected', 'Acquisition Date': '2024-01-15', 'Warranty Expiry Date': '2027-01-15',
        'Product Make/Model': 'Dell Latitude 5430', 'Product Type': 'Laptop', 'Serial Number': 'APX-SN-54301',
        'Adaptor Serial Number': 'APX-AD-001', 'OS': 'Windows 11 Enterprise', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'Intel Core i7-1265U 2.7 GHz', 'Total Memory': '16384 MB', 'HardDisk Capacity': '512 GB NVMe SSD',
        'MonitorMake/Model': 'Dell U2422H', 'Monitor Serial Number': 'APX-MN-101', 'User': 'John Doe',
        'Employee ID': 'EMP001', 'Level': 'L4', 'Category': 'Officer', 'Designation': 'Enterprise Architect',
        'Email': 'john.doe@apexcorp.demo', 'Mobile': '9876543210', 'Department': 'IT', 'Section': 'Enterprise Systems',
        'Location': 'HQ - Tech Center', 'Description': 'Primary development laptop', 'Purchase Order Number': 'PO-2024-001',
        'Purchase Date': '2024-01-10', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100101, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-LAP-102', 'Asset Type': 'Laptop', 'Asset Category': 'Standard Laptop', 'Asset State': 'In Use',
        'Connected or Isolated': 'Connected', 'Acquisition Date': '2024-02-10', 'Warranty Expiry Date': '2027-02-10',
        'Product Make/Model': 'HP EliteBook 840 G9', 'Product Type': 'Laptop', 'Serial Number': 'APX-SN-84002',
        'Adaptor Serial Number': 'APX-AD-002', 'OS': 'Windows 11 Enterprise', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'Intel Core i5-1245U 2.5 GHz', 'Total Memory': '16384 MB', 'HardDisk Capacity': '512 GB SSD',
        'MonitorMake/Model': 'HP E24 G4', 'Monitor Serial Number': 'APX-MN-102', 'User': 'Jane Smith',
        'Employee ID': 'EMP002', 'Level': 'L3', 'Category': 'Officer', 'Designation': 'Financial Controller',
        'Email': 'jane.smith@apexcorp.demo', 'Mobile': '9876543211', 'Department': 'Finance', 'Section': 'Corporate Accounts',
        'Location': 'HQ - Tech Center', 'Description': 'Finance reporting laptop', 'Purchase Order Number': 'PO-2024-002',
        'Purchase Date': '2024-02-01', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100102, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-LAP-103', 'Asset Type': 'Laptop', 'Asset Category': 'Standard Laptop', 'Asset State': 'In Use',
        'Connected or Isolated': 'Connected', 'Acquisition Date': '2024-03-05', 'Warranty Expiry Date': '2027-03-05',
        'Product Make/Model': 'Lenovo ThinkPad T14', 'Product Type': 'Laptop', 'Serial Number': 'APX-SN-14003',
        'Adaptor Serial Number': 'APX-AD-003', 'OS': 'Windows 11 Enterprise', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'AMD Ryzen 7 PRO 6850U', 'Total Memory': '32768 MB', 'HardDisk Capacity': '1024 GB NVMe SSD',
        'MonitorMake/Model': 'Lenovo ThinkVision T24i', 'Monitor Serial Number': 'APX-MN-103', 'User': 'Alex Johnson',
        'Employee ID': 'EMP003', 'Level': 'L3', 'Category': 'Officer', 'Designation': 'Operations Lead',
        'Email': 'alex.johnson@apexcorp.demo', 'Mobile': '9876543212', 'Department': 'Operations', 'Section': 'Plant Logistics',
        'Location': 'Plant Alpha', 'Description': 'Operations control workstation', 'Purchase Order Number': 'PO-2024-003',
        'Purchase Date': '2024-02-20', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100103, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-LAP-104', 'Asset Type': 'Laptop', 'Asset Category': 'Standard Laptop', 'Asset State': 'In Use',
        'Connected or Isolated': 'Connected', 'Acquisition Date': '2024-03-12', 'Warranty Expiry Date': '2027-03-12',
        'Product Make/Model': 'Dell Latitude 5430', 'Product Type': 'Laptop', 'Serial Number': 'APX-SN-54304',
        'Adaptor Serial Number': 'APX-AD-004', 'OS': 'Windows 11 Enterprise', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'Intel Core i5-1245U 2.5 GHz', 'Total Memory': '16384 MB', 'HardDisk Capacity': '512 GB SSD',
        'MonitorMake/Model': 'Dell P2419H', 'Monitor Serial Number': 'APX-MN-104', 'User': 'Rahul Sharma',
        'Employee ID': 'EMP004', 'Level': 'L4', 'Category': 'Officer', 'Designation': 'SCM Lead Manager',
        'Email': 'rahul.sharma@apexcorp.demo', 'Mobile': '9876543213', 'Department': 'Supply Chain', 'Section': 'Procurement',
        'Location': 'HQ - Tech Center', 'Description': 'Procurement & vendor management laptop', 'Purchase Order Number': 'PO-2024-004',
        'Purchase Date': '2024-03-01', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100104, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-LAP-105', 'Asset Type': 'Laptop', 'Asset Category': 'Ultrabook', 'Asset State': 'In Use',
        'Connected or Isolated': 'Connected', 'Acquisition Date': '2024-04-01', 'Warranty Expiry Date': '2027-04-01',
        'Product Make/Model': 'HP EliteBook 840 G9', 'Product Type': 'Laptop', 'Serial Number': 'APX-SN-84005',
        'Adaptor Serial Number': 'APX-AD-005', 'OS': 'Windows 11 Enterprise', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'Intel Core i5-1245U 2.5 GHz', 'Total Memory': '16384 MB', 'HardDisk Capacity': '512 GB SSD',
        'MonitorMake/Model': 'HP E24 G4', 'Monitor Serial Number': 'APX-MN-105', 'User': 'Priya Patel',
        'Employee ID': 'EMP005', 'Level': 'L2', 'Category': 'Associate', 'Designation': 'HR Business Partner',
        'Email': 'priya.patel@apexcorp.demo', 'Mobile': '9876543214', 'Department': 'HR', 'Section': 'Talent Management',
        'Location': 'HQ - Tech Center', 'Description': 'HR & payroll workstation', 'Purchase Order Number': 'PO-2024-005',
        'Purchase Date': '2024-03-15', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100105, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-DESK-201', 'Asset Type': 'Desktop', 'Asset Category': 'Desktop Workstation', 'Asset State': 'In Use',
        'Connected or Isolated': 'Connected', 'Acquisition Date': '2023-11-10', 'Warranty Expiry Date': '2026-11-10',
        'Product Make/Model': 'Dell OptiPlex 7090', 'Product Type': 'Desktop', 'Serial Number': 'APX-SN-70901',
        'Adaptor Serial Number': '', 'OS': 'Windows 11 Pro', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'Intel Core i7-11700 2.50 GHz', 'Total Memory': '32768 MB', 'HardDisk Capacity': '1024 GB SSD',
        'MonitorMake/Model': 'Dell P2722H', 'Monitor Serial Number': 'APX-MN-201', 'User': 'Michael Brown',
        'Employee ID': 'EMP006', 'Level': 'L3', 'Category': 'Officer', 'Designation': 'DevOps & Cloud Engineer',
        'Email': 'michael.brown@apexcorp.demo', 'Mobile': '9876543215', 'Department': 'IT', 'Section': 'Infrastructure',
        'Location': 'Tech Hub - Austin', 'Description': 'High-performance DevOps workstation', 'Purchase Order Number': 'PO-2023-110',
        'Purchase Date': '2023-11-01', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100201, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-DESK-202', 'Asset Type': 'Desktop', 'Asset Category': 'Standard Desktop', 'Asset State': 'In Use',
        'Connected or Isolated': 'Connected', 'Acquisition Date': '2023-12-05', 'Warranty Expiry Date': '2026-12-05',
        'Product Make/Model': 'HP ProDesk 600 G6', 'Product Type': 'Desktop', 'Serial Number': 'APX-SN-60002',
        'Adaptor Serial Number': '', 'OS': 'Windows 11 Pro', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'Intel Core i5-10500 3.10 GHz', 'Total Memory': '16384 MB', 'HardDisk Capacity': '512 GB SSD',
        'MonitorMake/Model': 'HP P24v G4', 'Monitor Serial Number': 'APX-MN-202', 'User': 'Emily Davis',
        'Employee ID': 'EMP007', 'Level': 'L2', 'Category': 'Officer', 'Designation': 'Senior Accountant',
        'Email': 'emily.davis@apexcorp.demo', 'Mobile': '9876543216', 'Department': 'Finance', 'Section': 'Accounts Payable',
        'Location': 'HQ - Tech Center', 'Description': 'Billing and invoice terminal', 'Purchase Order Number': 'PO-2023-120',
        'Purchase Date': '2023-11-20', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100202, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-DESK-203', 'Asset Type': 'Desktop', 'Asset Category': 'Standard Desktop', 'Asset State': 'In Use',
        'Connected or Isolated': 'Connected', 'Acquisition Date': '2024-01-20', 'Warranty Expiry Date': '2027-01-20',
        'Product Make/Model': 'Lenovo ThinkCentre M70q', 'Product Type': 'Desktop', 'Serial Number': 'APX-SN-70003',
        'Adaptor Serial Number': '', 'OS': 'Windows 11 Pro', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'Intel Core i5-12400T 2.0 GHz', 'Total Memory': '16384 MB', 'HardDisk Capacity': '512 GB SSD',
        'MonitorMake/Model': 'Lenovo T24d', 'Monitor Serial Number': 'APX-MN-203', 'User': 'David Wilson',
        'Employee ID': 'EMP008', 'Level': 'L4', 'Category': 'Officer', 'Designation': 'Plant Maintenance Head',
        'Email': 'david.wilson@apexcorp.demo', 'Mobile': '9876543217', 'Department': 'Operations', 'Section': 'Plant Operations',
        'Location': 'Plant Alpha', 'Description': 'Plant automation terminal', 'Purchase Order Number': 'PO-2024-015',
        'Purchase Date': '2024-01-10', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100203, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-LAP-106', 'Asset Type': 'Laptop', 'Asset Category': 'Standard Laptop', 'Asset State': 'In Use',
        'Connected or Isolated': 'Connected', 'Acquisition Date': '2024-02-18', 'Warranty Expiry Date': '2027-02-18',
        'Product Make/Model': 'Dell Latitude 5430', 'Product Type': 'Laptop', 'Serial Number': 'APX-SN-54306',
        'Adaptor Serial Number': 'APX-AD-006', 'OS': 'Windows 11 Enterprise', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'Intel Core i5-1245U 2.5 GHz', 'Total Memory': '16384 MB', 'HardDisk Capacity': '512 GB SSD',
        'MonitorMake/Model': 'Dell P2419H', 'Monitor Serial Number': 'APX-MN-106', 'User': 'Sarah Miller',
        'Employee ID': 'EMP009', 'Level': 'L2', 'Category': 'Associate', 'Designation': 'Procurement Specialist',
        'Email': 'sarah.miller@apexcorp.demo', 'Mobile': '9876543218', 'Department': 'Supply Chain', 'Section': 'Procurement',
        'Location': 'Warehouse North', 'Description': 'Material procurement laptop', 'Purchase Order Number': 'PO-2024-022',
        'Purchase Date': '2024-02-05', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100106, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-LAP-107', 'Asset Type': 'Laptop', 'Asset Category': 'Mobile Workstation', 'Asset State': 'In Use',
        'Connected or Isolated': 'Connected', 'Acquisition Date': '2024-03-01', 'Warranty Expiry Date': '2027-03-01',
        'Product Make/Model': 'Lenovo ThinkPad P14s', 'Product Type': 'Laptop', 'Serial Number': 'APX-SN-14007',
        'Adaptor Serial Number': 'APX-AD-007', 'OS': 'Windows 11 Enterprise', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'AMD Ryzen 7 PRO 7840U', 'Total Memory': '32768 MB', 'HardDisk Capacity': '1024 GB NVMe SSD',
        'MonitorMake/Model': 'Lenovo T27q', 'Monitor Serial Number': 'APX-MN-107', 'User': 'James Taylor',
        'Employee ID': 'EMP010', 'Level': 'L3', 'Category': 'Officer', 'Designation': 'Network Administrator',
        'Email': 'james.taylor@apexcorp.demo', 'Mobile': '9876543219', 'Department': 'IT', 'Section': 'Infrastructure',
        'Location': 'Tech Hub - Austin', 'Description': 'Network monitoring and infrastructure laptop', 'Purchase Order Number': 'PO-2024-030',
        'Purchase Date': '2024-02-20', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100107, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-SRV-301', 'Asset Type': 'Server', 'Asset Category': 'Rack Server', 'Asset State': 'In Use',
        'Connected or Isolated': 'Connected', 'Acquisition Date': '2023-06-15', 'Warranty Expiry Date': '2028-06-15',
        'Product Make/Model': 'Dell PowerEdge R740', 'Product Type': 'Server', 'Serial Number': 'APX-SRV-7401',
        'Adaptor Serial Number': '', 'OS': 'Red Hat Enterprise Linux 9.2', 'OS version': '9.2', 'OS build Version': '5.14.0',
        'Processor Name/Speed': '2x Intel Xeon Gold 6248R 3.0 GHz', 'Total Memory': '131072 MB', 'HardDisk Capacity': '8x 1.92TB SAS SSD RAID 10',
        'MonitorMake/Model': '', 'Monitor Serial Number': '', 'User': 'John Doe',
        'Employee ID': 'EMP001', 'Level': 'L4', 'Category': 'Officer', 'Designation': 'Enterprise Architect',
        'Email': 'john.doe@apexcorp.demo', 'Mobile': '9876543210', 'Department': 'IT', 'Section': 'Data Center',
        'Location': 'HQ - Data Center', 'Description': 'Core SAP Application Production Server', 'Purchase Order Number': 'PO-2023-050',
        'Purchase Date': '2023-05-15', 'Supply Vendor': 'Enterprise Hardware Systems', 'SAP CODE': 100301, 'Encryption Status': 'Hardware Encrypted'
    },
    {
        'Asset Tag': 'APX-NAS-401', 'Asset Type': 'NAS Storage', 'Asset Category': 'Network Storage', 'Asset State': 'In Use',
        'Connected or Isolated': 'Connected', 'Acquisition Date': '2023-08-20', 'Warranty Expiry Date': '2026-08-20',
        'Product Make/Model': 'Synology RackStation RS3621xs+', 'Product Type': 'Storage', 'Serial Number': 'APX-NAS-3621',
        'Adaptor Serial Number': '', 'OS': 'DSM 7.2', 'OS version': '7.2', 'OS build Version': '64570',
        'Processor Name/Speed': 'Intel Xeon D-1541 2.1 GHz', 'Total Memory': '65536 MB', 'HardDisk Capacity': '12x 16TB Enterprise HDD',
        'MonitorMake/Model': '', 'Monitor Serial Number': '', 'User': 'Michael Brown',
        'Employee ID': 'EMP006', 'Level': 'L3', 'Category': 'Officer', 'Designation': 'DevOps & Cloud Engineer',
        'Email': 'michael.brown@apexcorp.demo', 'Mobile': '9876543215', 'Department': 'IT', 'Section': 'Data Center',
        'Location': 'HQ - Data Center', 'Description': 'Primary backup repository NAS', 'Purchase Order Number': 'PO-2023-085',
        'Purchase Date': '2023-08-01', 'Supply Vendor': 'Enterprise Hardware Systems', 'SAP CODE': 100401, 'Encryption Status': 'AES-256'
    },
    # IT Stock items (No assigned user)
    {
        'Asset Tag': 'APX-LAP-108', 'Asset Type': 'Laptop', 'Asset Category': 'Standard Laptop', 'Asset State': 'IT Stock',
        'Connected or Isolated': 'Isolated', 'Acquisition Date': '2024-04-10', 'Warranty Expiry Date': '2027-04-10',
        'Product Make/Model': 'Dell Latitude 5430', 'Product Type': 'Laptop', 'Serial Number': 'APX-SN-54308',
        'Adaptor Serial Number': 'APX-AD-008', 'OS': 'Windows 11 Enterprise', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'Intel Core i5-1245U 2.5 GHz', 'Total Memory': '16384 MB', 'HardDisk Capacity': '512 GB SSD',
        'MonitorMake/Model': '', 'Monitor Serial Number': '', 'User': None,
        'Employee ID': None, 'Level': None, 'Category': None, 'Designation': None,
        'Email': None, 'Mobile': None, 'Department': 'IT', 'Section': 'IT Operations',
        'Location': 'HQ - Tech Center', 'Description': 'Spare pool laptop ready for deployment', 'Purchase Order Number': 'PO-2024-040',
        'Purchase Date': '2024-04-01', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100108, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-LAP-109', 'Asset Type': 'Laptop', 'Asset Category': 'Standard Laptop', 'Asset State': 'IT Stock',
        'Connected or Isolated': 'Isolated', 'Acquisition Date': '2024-04-10', 'Warranty Expiry Date': '2027-04-10',
        'Product Make/Model': 'HP EliteBook 840 G9', 'Product Type': 'Laptop', 'Serial Number': 'APX-SN-84009',
        'Adaptor Serial Number': 'APX-AD-009', 'OS': 'Windows 11 Enterprise', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'Intel Core i5-1245U 2.5 GHz', 'Total Memory': '16384 MB', 'HardDisk Capacity': '512 GB SSD',
        'MonitorMake/Model': '', 'Monitor Serial Number': '', 'User': None,
        'Employee ID': None, 'Level': None, 'Category': None, 'Designation': None,
        'Email': None, 'Mobile': None, 'Department': 'IT', 'Section': 'IT Operations',
        'Location': 'Tech Hub - Austin', 'Description': 'Spare pool laptop in Austin IT locker', 'Purchase Order Number': 'PO-2024-040',
        'Purchase Date': '2024-04-01', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100109, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-DESK-204', 'Asset Type': 'Desktop', 'Asset Category': 'Standard Desktop', 'Asset State': 'IT Stock',
        'Connected or Isolated': 'Isolated', 'Acquisition Date': '2024-01-15', 'Warranty Expiry Date': '2027-01-15',
        'Product Make/Model': 'Dell OptiPlex 7090', 'Product Type': 'Desktop', 'Serial Number': 'APX-SN-70904',
        'Adaptor Serial Number': '', 'OS': 'Windows 11 Pro', 'OS version': '23H2', 'OS build Version': '22631.3007',
        'Processor Name/Speed': 'Intel Core i5-11500 2.7 GHz', 'Total Memory': '16384 MB', 'HardDisk Capacity': '512 GB SSD',
        'MonitorMake/Model': '', 'Monitor Serial Number': '', 'User': None,
        'Employee ID': None, 'Level': None, 'Category': None, 'Designation': None,
        'Email': None, 'Mobile': None, 'Department': 'Operations', 'Section': 'Plant IT',
        'Location': 'Plant Alpha', 'Description': 'Replacement terminal for plant floor', 'Purchase Order Number': 'PO-2024-010',
        'Purchase Date': '2024-01-05', 'Supply Vendor': 'Apex Infotech Solutions', 'SAP CODE': 100204, 'Encryption Status': 'BitLocker Enabled'
    },
    {
        'Asset Tag': 'APX-SRV-302', 'Asset Type': 'Server', 'Asset Category': 'Rack Server', 'Asset State': 'IT Stock',
        'Connected or Isolated': 'Isolated', 'Acquisition Date': '2024-02-01', 'Warranty Expiry Date': '2029-02-01',
        'Product Make/Model': 'Dell PowerEdge R640', 'Product Type': 'Server', 'Serial Number': 'APX-SRV-6402',
        'Adaptor Serial Number': '', 'OS': 'Red Hat Enterprise Linux 9.2', 'OS version': '9.2', 'OS build Version': '5.14.0',
        'Processor Name/Speed': '2x Intel Xeon Silver 4314 2.4 GHz', 'Total Memory': '65536 MB', 'HardDisk Capacity': '4x 960GB SAS SSD',
        'MonitorMake/Model': '', 'Monitor Serial Number': '', 'User': None,
        'Employee ID': None, 'Level': None, 'Category': None, 'Designation': None,
        'Email': None, 'Mobile': None, 'Department': 'IT', 'Section': 'Data Center',
        'Location': 'HQ - Data Center', 'Description': 'Staging DR Server node', 'Purchase Order Number': 'PO-2024-020',
        'Purchase Date': '2024-01-20', 'Supply Vendor': 'Enterprise Hardware Systems', 'SAP CODE': 100302, 'Encryption Status': 'Hardware Encrypted'
    }
]

df_asset = pd.DataFrame(asset_rows)
df_asset.to_csv(os.path.join(sample_dir, 'mock_asset_data.csv'), index=False)
df_asset.to_excel(os.path.join(sample_dir, 'mock_asset_data.xlsx'), index=False)
print('Mock Asset Dataset created:', len(df_asset), 'rows')

# 2. MOCK SAP USER MASTER
sap_users = [
    {'SAP ID': 'EMP001', 'Username': 'John Doe', 'Department': 'IT', 'Reporting Manager': 'Sarah Connor', 'User Created On': '2023-01-10', 'User Type': 'Dialog User', 'Valid From': '2023-01-10', 'Valid To': '2030-12-31'},
    {'SAP ID': 'EMP002', 'Username': 'Jane Smith', 'Department': 'Finance', 'Reporting Manager': 'Arthur Pendelton', 'User Created On': '2023-02-15', 'User Type': 'Dialog User', 'Valid From': '2023-02-15', 'Valid To': '2030-12-31'},
    {'SAP ID': 'EMP003', 'Username': 'Alex Johnson', 'Department': 'Operations', 'Reporting Manager': 'Marcus Vance', 'User Created On': '2023-03-01', 'User Type': 'Dialog User', 'Valid From': '2023-03-01', 'Valid To': '2030-12-31'},
    {'SAP ID': 'EMP004', 'Username': 'Rahul Sharma', 'Department': 'Supply Chain', 'Reporting Manager': 'Saurabh Verma', 'User Created On': '2023-04-12', 'User Type': 'Dialog User', 'Valid From': '2023-04-12', 'Valid To': '2030-12-31'},
    {'SAP ID': 'EMP005', 'Username': 'Priya Patel', 'Department': 'HR', 'Reporting Manager': 'Elena Rostova', 'User Created On': '2023-05-20', 'User Type': 'Dialog User', 'Valid From': '2023-05-20', 'Valid To': '2030-12-31'},
    {'SAP ID': 'EMP006', 'Username': 'Michael Brown', 'Department': 'IT', 'Reporting Manager': 'John Doe', 'User Created On': '2023-06-01', 'User Type': 'Dialog User', 'Valid From': '2023-06-01', 'Valid To': '2030-12-31'},
    {'SAP ID': 'EMP007', 'Username': 'Emily Davis', 'Department': 'Finance', 'Reporting Manager': 'Jane Smith', 'User Created On': '2023-07-15', 'User Type': 'Dialog User', 'Valid From': '2023-07-15', 'Valid To': '2030-12-31'},
    {'SAP ID': 'EMP008', 'Username': 'David Wilson', 'Department': 'Operations', 'Reporting Manager': 'Alex Johnson', 'User Created On': '2023-08-10', 'User Type': 'Dialog User', 'Valid From': '2023-08-10', 'Valid To': '2030-12-31'},
    {'SAP ID': 'EMP009', 'Username': 'Sarah Miller', 'Department': 'Supply Chain', 'Reporting Manager': 'Rahul Sharma', 'User Created On': '2023-09-05', 'User Type': 'Dialog User', 'Valid From': '2023-09-05', 'Valid To': '2030-12-31'},
    {'SAP ID': 'EMP010', 'Username': 'James Taylor', 'Department': 'IT', 'Reporting Manager': 'John Doe', 'User Created On': '2023-10-01', 'User Type': 'Dialog User', 'Valid From': '2023-10-01', 'Valid To': '2030-12-31'},
    {'SAP ID': 'BATCH_SVC', 'Username': 'Background Batch Service', 'Department': 'IT', 'Reporting Manager': 'System Admin', 'User Created On': '2023-01-01', 'User Type': 'System User', 'Valid From': '2023-01-01', 'Valid To': '2035-12-31'},
    {'SAP ID': 'RFC_INTEG', 'Username': 'SAP RFC Integration User', 'Department': 'IT', 'Reporting Manager': 'System Admin', 'User Created On': '2023-01-01', 'User Type': 'System User', 'Valid From': '2023-01-01', 'Valid To': '2035-12-31'}
]

df_users = pd.DataFrame(sap_users)
df_users.to_excel(os.path.join(sample_dir, 'mock_sap_users.xlsx'), index=False)
print('Mock SAP User Master created:', len(df_users), 'rows')

# 3. MOCK SAP ACCESS / ROLES LIST
sap_access = [
    # EMP001 (IT)
    {'SAP ID': 'EMP001', 'Username': 'John Doe', 'Department': 'IT', 'Reporting Manager': 'Sarah Connor', 'Role': 'APEX_IT_ADMIN', 'Tcode': 'SU01', 'Tcode Description': 'User Maintenance'},
    {'SAP ID': 'EMP001', 'Username': 'John Doe', 'Department': 'IT', 'Reporting Manager': 'Sarah Connor', 'Role': 'APEX_IT_ADMIN', 'Tcode': 'PFCG', 'Tcode Description': 'Role Maintenance'},
    {'SAP ID': 'EMP001', 'Username': 'John Doe', 'Department': 'IT', 'Reporting Manager': 'Sarah Connor', 'Role': 'APEX_IT_ADMIN', 'Tcode': 'SM20', 'Tcode Description': 'Security Audit Log'},
    {'SAP ID': 'EMP001', 'Username': 'John Doe', 'Department': 'IT', 'Reporting Manager': 'Sarah Connor', 'Role': 'APEX_IT_ADMIN', 'Tcode': 'SM50', 'Tcode Description': 'Work Process Overview'},
    {'SAP ID': 'EMP001', 'Username': 'John Doe', 'Department': 'IT', 'Reporting Manager': 'Sarah Connor', 'Role': 'APEX_IT_ADMIN', 'Tcode': 'ST03N', 'Tcode Description': 'Workload Monitor'},
    # EMP002 (Finance)
    {'SAP ID': 'EMP002', 'Username': 'Jane Smith', 'Department': 'Finance', 'Reporting Manager': 'Arthur Pendelton', 'Role': 'APEX_FIN_LEAD', 'Tcode': 'FB01', 'Tcode Description': 'Post Document'},
    {'SAP ID': 'EMP002', 'Username': 'Jane Smith', 'Department': 'Finance', 'Reporting Manager': 'Arthur Pendelton', 'Role': 'APEX_FIN_LEAD', 'Tcode': 'FB03', 'Tcode Description': 'Display Document'},
    {'SAP ID': 'EMP002', 'Username': 'Jane Smith', 'Department': 'Finance', 'Reporting Manager': 'Arthur Pendelton', 'Role': 'APEX_FIN_LEAD', 'Tcode': 'FBL1N', 'Tcode Description': 'Vendor Line Items'},
    {'SAP ID': 'EMP002', 'Username': 'Jane Smith', 'Department': 'Finance', 'Reporting Manager': 'Arthur Pendelton', 'Role': 'APEX_FIN_LEAD', 'Tcode': 'FBL3N', 'Tcode Description': 'G/L Account Line Items'},
    {'SAP ID': 'EMP002', 'Username': 'Jane Smith', 'Department': 'Finance', 'Reporting Manager': 'Arthur Pendelton', 'Role': 'APEX_FIN_LEAD', 'Tcode': 'FBL5N', 'Tcode Description': 'Customer Line Items'},
    # EMP003 (Operations)
    {'SAP ID': 'EMP003', 'Username': 'Alex Johnson', 'Department': 'Operations', 'Reporting Manager': 'Marcus Vance', 'Role': 'APEX_OPS_MGR', 'Tcode': 'CO01', 'Tcode Description': 'Create Production Order'},
    {'SAP ID': 'EMP003', 'Username': 'Alex Johnson', 'Department': 'Operations', 'Reporting Manager': 'Marcus Vance', 'Role': 'APEX_OPS_MGR', 'Tcode': 'CO03', 'Tcode Description': 'Display Production Order'},
    {'SAP ID': 'EMP003', 'Username': 'Alex Johnson', 'Department': 'Operations', 'Reporting Manager': 'Marcus Vance', 'Role': 'APEX_OPS_MGR', 'Tcode': 'MIGO', 'Tcode Description': 'Goods Movement'},
    {'SAP ID': 'EMP003', 'Username': 'Alex Johnson', 'Department': 'Operations', 'Reporting Manager': 'Marcus Vance', 'Role': 'APEX_OPS_MGR', 'Tcode': 'MB51', 'Tcode Description': 'Material Doc. List'},
    # EMP004 (Supply Chain)
    {'SAP ID': 'EMP004', 'Username': 'Rahul Sharma', 'Department': 'Supply Chain', 'Reporting Manager': 'Saurabh Verma', 'Role': 'APEX_SCM_MGR', 'Tcode': 'ME21N', 'Tcode Description': 'Create Purchase Order'},
    {'SAP ID': 'EMP004', 'Username': 'Rahul Sharma', 'Department': 'Supply Chain', 'Reporting Manager': 'Saurabh Verma', 'Role': 'APEX_SCM_MGR', 'Tcode': 'ME22N', 'Tcode Description': 'Change Purchase Order'},
    {'SAP ID': 'EMP004', 'Username': 'Rahul Sharma', 'Department': 'Supply Chain', 'Reporting Manager': 'Saurabh Verma', 'Role': 'APEX_SCM_MGR', 'Tcode': 'ME23N', 'Tcode Description': 'Display Purchase Order'},
    {'SAP ID': 'EMP004', 'Username': 'Rahul Sharma', 'Department': 'Supply Chain', 'Reporting Manager': 'Saurabh Verma', 'Role': 'APEX_SCM_MGR', 'Tcode': 'MM03', 'Tcode Description': 'Display Material'},
    # EMP005 (HR)
    {'SAP ID': 'EMP005', 'Username': 'Priya Patel', 'Department': 'HR', 'Reporting Manager': 'Elena Rostova', 'Role': 'APEX_HR_SPEC', 'Tcode': 'PA20', 'Tcode Description': 'Display HR Master Data'},
    {'SAP ID': 'EMP005', 'Username': 'Priya Patel', 'Department': 'HR', 'Reporting Manager': 'Elena Rostova', 'Role': 'APEX_HR_SPEC', 'Tcode': 'PA30', 'Tcode Description': 'Maintain HR Master Data'},
    {'SAP ID': 'EMP005', 'Username': 'Priya Patel', 'Department': 'HR', 'Reporting Manager': 'Elena Rostova', 'Role': 'APEX_HR_SPEC', 'Tcode': 'PPOME', 'Tcode Description': 'Change Organization and Staffing'},
    # EMP006 (IT)
    {'SAP ID': 'EMP006', 'Username': 'Michael Brown', 'Department': 'IT', 'Reporting Manager': 'John Doe', 'Role': 'APEX_IT_DEV', 'Tcode': 'SE16', 'Tcode Description': 'Data Browser'},
    {'SAP ID': 'EMP006', 'Username': 'Michael Brown', 'Department': 'IT', 'Reporting Manager': 'John Doe', 'Role': 'APEX_IT_DEV', 'Tcode': 'SE38', 'Tcode Description': 'ABAP Editor'},
    # EMP007 (Finance)
    {'SAP ID': 'EMP007', 'Username': 'Emily Davis', 'Department': 'Finance', 'Reporting Manager': 'Jane Smith', 'Role': 'APEX_FIN_USER', 'Tcode': 'FB03', 'Tcode Description': 'Display Document'},
    {'SAP ID': 'EMP007', 'Username': 'Emily Davis', 'Department': 'Finance', 'Reporting Manager': 'Jane Smith', 'Role': 'APEX_FIN_USER', 'Tcode': 'FBL1N', 'Tcode Description': 'Vendor Line Items'},
    # EMP008 (Operations)
    {'SAP ID': 'EMP008', 'Username': 'David Wilson', 'Department': 'Operations', 'Reporting Manager': 'Alex Johnson', 'Role': 'APEX_OPS_USER', 'Tcode': 'CO03', 'Tcode Description': 'Display Production Order'},
    {'SAP ID': 'EMP008', 'Username': 'David Wilson', 'Department': 'Operations', 'Reporting Manager': 'Alex Johnson', 'Role': 'APEX_OPS_USER', 'Tcode': 'MIGO', 'Tcode Description': 'Goods Movement'},
    # EMP009 (Supply Chain)
    {'SAP ID': 'EMP009', 'Username': 'Sarah Miller', 'Department': 'Supply Chain', 'Reporting Manager': 'Rahul Sharma', 'Role': 'APEX_SCM_USER', 'Tcode': 'ME23N', 'Tcode Description': 'Display Purchase Order'},
    {'SAP ID': 'EMP009', 'Username': 'Sarah Miller', 'Department': 'Supply Chain', 'Reporting Manager': 'Rahul Sharma', 'Role': 'APEX_SCM_USER', 'Tcode': 'MM03', 'Tcode Description': 'Display Material'},
    # EMP010 (IT)
    {'SAP ID': 'EMP010', 'Username': 'James Taylor', 'Department': 'IT', 'Reporting Manager': 'John Doe', 'Role': 'APEX_IT_SEC', 'Tcode': 'SM20', 'Tcode Description': 'Security Audit Log'}
]

df_access = pd.DataFrame(sap_access)
df_access.to_excel(os.path.join(sample_dir, 'mock_sap_access.xlsx'), index=False)
print('Mock SAP Access List created:', len(df_access), 'rows')

# 4. MOCK SM20 AUDIT LOGS (Multi-month: Apr, May, Jun 2026)
sm20_entries = []
log_dates = [
    '2026-04-05', '2026-04-06', '2026-04-12', '2026-04-18', '2026-04-25',
    '2026-05-02', '2026-05-10', '2026-05-15', '2026-05-22', '2026-05-28',
    '2026-06-03', '2026-06-11', '2026-06-18', '2026-06-24', '2026-06-29'
]

# For each dialog user, generate login records and transaction execution records
user_tcodes = {
    'EMP001': [('SU01', 'APX-LAP-101'), ('PFCG', 'APX-LAP-101'), ('SM20', 'APX-LAP-101')],
    'EMP002': [('FB03', 'APX-LAP-102'), ('FBL1N', 'APX-LAP-102'), ('FB01', 'APX-LAP-102')],
    'EMP003': [('CO03', 'APX-LAP-103'), ('MIGO', 'APX-LAP-103')],
    'EMP004': [('ME21N', 'APX-LAP-104'), ('ME23N', 'APX-LAP-104'), ('MM03', 'APX-LAP-104')],
    'EMP005': [('PA20', 'APX-LAP-105'), ('PA30', 'APX-LAP-105')],
    'EMP006': [('SE16', 'APX-DESK-201'), ('SE38', 'APX-DESK-201')],
    'EMP007': [('FB03', 'APX-DESK-202'), ('FBL1N', 'APX-DESK-202')],
    'EMP008': [('CO03', 'APX-DESK-203'), ('MIGO', 'APX-DESK-203')],
    'EMP009': [('ME23N', 'APX-LAP-106'), ('MM03', 'APX-LAP-106')],
    'EMP010': [('SM20', 'APX-LAP-107')]
}

for i, dt in enumerate(log_dates):
    for uid, tlist in user_tcodes.items():
        term = tlist[0][1]
        # 1. Successful Logon Entry
        sm20_entries.append({
            'Creation Date': dt,
            'Creation time of audit entry': f'{9 + (i % 2):02d}:{10 + (i * 3) % 40:02d}:15',
            'Client': '300',
            'User Name': uid,
            'Terminal name': term,
            'Triggering Transaction Code': 'S000',
            'Program': 'SAPMSYST',
            'Audit Log Msg. Text': 'Logon successful (type=A, method=P )',
            'Reference to Long Version of a Text': '',
            'SAP process': 'D',
            'Work Process Number': '012',
            'Variable Message Data': 'A'
        })
        # 2. Transaction started entries
        for tcode, _ in tlist:
            sm20_entries.append({
                'Creation Date': dt,
                'Creation time of audit entry': f'{10 + (i % 4):02d}:{15 + (i * 5) % 40:02d}:30',
                'Client': '300',
                'User Name': uid,
                'Terminal name': term,
                'Triggering Transaction Code': 'SESSION_MANAGER',
                'Program': 'SAPLSMTR_NAVIGATION',
                'Audit Log Msg. Text': f'Transaction {tcode} started.',
                'Reference to Long Version of a Text': '',
                'SAP process': 'D',
                'Work Process Number': '015',
                'Variable Message Data': tcode
            })

# Add a few unassigned terminal entries for Login Violation detection demo:
sm20_entries.append({
    'Creation Date': '2026-05-18',
    'Creation time of audit entry': '22:45:10',
    'Client': '300',
    'User Name': 'EMP002',
    'Terminal name': 'APX-LAP-105', # Jane Smith (Finance) logging in from Priya's HR laptop
    'Triggering Transaction Code': 'S000',
    'Program': 'SAPMSYST',
    'Audit Log Msg. Text': 'Logon successful (type=A, method=P )',
    'Reference to Long Version of a Text': '',
    'SAP process': 'D',
    'Work Process Number': '008',
    'Variable Message Data': 'A'
})
sm20_entries.append({
    'Creation Date': '2026-06-12',
    'Creation time of audit entry': '23:15:00',
    'Client': '300',
    'User Name': 'EMP004',
    'Terminal name': 'APX-DESK-202', # Rahul Sharma logging in from Finance Desktop
    'Triggering Transaction Code': 'S000',
    'Program': 'SAPMSYST',
    'Audit Log Msg. Text': 'Logon successful (type=A, method=P )',
    'Reference to Long Version of a Text': '',
    'SAP process': 'D',
    'Work Process Number': '004',
    'Variable Message Data': 'A'
})

df_sm20 = pd.DataFrame(sm20_entries)
df_sm20.to_excel(os.path.join(sample_dir, 'mock_sm20_audit_log.xlsx'), index=False)
print('Mock SM20 Audit Log created:', len(df_sm20), 'rows')

# 5. MOCK LOGIN VIOLATION REPORT DATASET (Usr Nam format)
df_login_report = df_sm20.copy().rename(columns={'User Name': 'Usr Nam'})
df_login_report.to_excel(os.path.join(sample_dir, 'mock_login_audit_report.xlsx'), index=False)
print('Mock Login Report dataset created:', len(df_login_report), 'rows')
