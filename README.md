# 📄 PDF-to-CSV Broken Arrangements

A tool to extract structured data from "Promised Payments Report" PDF files into CSV format. It **skips `Paid In Full` and `Settled In Full` statuses**, handles a variety of table formats and row patterns, and can run as a Streamlit web app or a local Python script.

---

## ✨ Features

- Converts Promised Payments PDF reports into easy-to-use CSV files
- Skips records with **Paid In Full** and **Settled In Full** statuses
- Handles various row formats and messy line patterns in PDFs (see below)
- Works as a **Streamlit web app** (browser) or standalone Python script (batch)
- **No coding required** for web app—just upload and download

---

## 🧩 How PDF Patterns Are Handled

This script is designed to robustly extract data even when PDF text lines are inconsistent. It looks for and processes these typical patterns:

- **Standard Table Row**  
123456 John Doe 5 06/17/2025 $100.00 Partial Payment Arrangement

pgsql
Copy
Edit
- ID, Name, Broken Promises, Date, Amount, Status

- **Row Without Broken Promises**  
123456 Jane Smith 06/17/2025 $250.00 Paid In Full
- ID, Name, Date, Amount, Status (Broken Promises missing)

- **Rows With Multi-Word Names or Status**  
Handles names with spaces, special characters, or multi-word statuses like "MONTHLY PAYMENT ARRG".

- **Irregular Spacing**  
Tolerant of varying numbers of spaces between columns.

- **Skip Patterns**  
Ignores header lines, page info, totals, and rows with "Paid In Full" or "Settled In Full".

**In plain English:**  
The script uses flexible regular expressions to find table-like rows. If the "broken promises" column is missing, it still grabs the right columns by checking for the date and amount patterns. If a line is not recognized, it can print a message so you know something was skipped for manual review.

---

## 🚀 Usage

### 1. Streamlit Web App
Run locally or deploy to [Streamlit Cloud](https://streamlit.io/cloud):

pip install -r requirements.txt
streamlit run pdftocsvbrokenarrangement.py
Upload your PDF in the browser interface.

Download your clean CSV!

2. Local Python Script

pip install -r requirements.txt
python pdftocsvbrokenarrangement.py
Edit the pdf_path variable in the script to match your file location.

🛠️ Requirements
Python 3.7+

pdfplumber

streamlit

pandas

📝 Project Files
pdftocsvbrokenarrangement.py — The main tool (works as app or script)

requirements.txt — All dependencies

README.md — This file!

🙋 Author
Hazel Santos
