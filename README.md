# 🏦 Tuborrr Dev Bank - Digital Banking Hub

A secure, multi-account desktop banking management portal built with Python. This system features persistent ledger logging, encrypted admin access controls, and inter-account wire transactions wrapped inside a refined modern user interface.

## 🎨 Visual Identity & Theme
The application utilizes a tailored dark mode palette optimized 
for maximum interface clarity and a premium financial portal aesthetic:
*   **Primary Highlights:** Deep Turquoise (`#1e847f`)
*   **Interactive Controls:** Tan Accent (`#ecc19c`)
*   **Interface Base:** Jet Black (`#000000`)

## ⚡ Core Features
*   **Algorithmic Account Lookup:** Real-time ledger indexing and historical record retrieval.
*   **Transactional Ledger Engine:** Fully tracking Deposits, Withdrawals, and Inter-Account Wire Transfers.
*   **Vault Master Console:** Secure administrator login interface allowing global asset oversight and systemic balancing.
*   **Local State Persistence:** Automated JSON encryption mapping for safe storage and retrieval of active user balances and transaction receipts.

## 🚀 Quick Start & Installation

### Prerequisites
Ensure you have Python 3.10+, packages listed on 'requirements.txt' and your virtual environment activated.

### 1. Clone & Navigate
```bash
git clone [https://github.com/Tuborrr-Dev/Bank-Desktop-Application-System.git](https://github.com/Tuborrr-Dev/Bank-Desktop-Application-System.git)
cd "BANKING SYSTEM"
2. Install Dependencies
Bash
pip install -r requirements.txt
3. Launch Core Infrastructure
Bash
python BS.py
📂 Architecture Overview
Banking_System.py: Main application loop containing the thread-safe Graphical User Interface and financial backend logic.

accounts.json: System state file handling real-time data persistence.

requirements.txt: System package dependency configurations.

