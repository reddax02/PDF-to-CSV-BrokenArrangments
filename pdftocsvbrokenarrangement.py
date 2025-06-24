import streamlit as st
import pdfplumber
import pandas as pd
import re
import io

st.set_page_config(page_title="PDF Promised Payments to CSV", layout="centered")

st.title("PDF Promised Payments Report → CSV Converter")

uploaded_file = st.file_uploader("Upload your PDF file", type=["pdf"])

SKIP_STATUSES = ["Paid In Full", "Settled In Full"]

def parse_pdf(pdf_bytes):
    rows = []
    skipped = []
    unmatched = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue
            for line in text.split("\n"):
                if re.search(
                    r'Worklist:|Total|Page|Date|Time|Promised Payments Report|Resolve Financial Recovery|Broken|Debtor ID|Debtor Name|Promises|Status|Amount',
                    line, re.IGNORECASE):
                    continue
                match = re.match(
                    r"^(\d{5,})\s+(.+?)\s+(\d{2}/\d{2}/\d{4})\s+\$?([\d,\.]+)\s+(.+)$",
                    line.strip()
                )
                if match:
                    debtor_id = match.group(1)
                    middle = match.group(2).strip()
                    date = match.group(3)
                    amount = match.group(4).replace(",", "")
                    status = match.group(5).strip()
                    split_middle = re.match(r"(.+)\s+(\d+)$", middle)
                    if split_middle:
                        name = split_middle.group(1).strip()
                        broken = split_middle.group(2)
                    else:
                        name = middle
                        broken = ""
                    if any(skip in status for skip in SKIP_STATUSES):
                        skipped.append([debtor_id, name, broken, date, amount, status])
                    else:
                        rows.append([debtor_id, name, broken, date, amount, status])
                elif len(line.strip()) > 10:
                    unmatched.append([line.strip()])
    columns = [
        "Debtor ID",
        "Debtor Name",
        "Broken Promises",
        "Promised Pmt Date",
        "Promised Pmt Amount",
        "Debtor Status"
    ]
    return pd.DataFrame(rows, columns=columns), pd.DataFrame(skipped, columns=columns), pd.DataFrame(unmatched, columns=["Unmatched Line"])

if uploaded_file is not None:
    st.info("Parsing PDF...")
    df, skipped_df, unmatched_df = parse_pdf(uploaded_file.read())
    st.success(f"Parsed {len(df)} rows!")
    st.dataframe(df)

    # Download link
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download as CSV",
        data=csv,
        file_name="promised_payments_report.csv",
        mime="text/csv"
    )

    if not skipped_df.empty:
        st.warning(f"{len(skipped_df)} rows were skipped (Paid/Settled In Full).")
        with st.expander("Show skipped rows"):
            st.dataframe(skipped_df)

    if not unmatched_df.empty:
        st.error(f"{len(unmatched_df)} lines were NOT matched and may need review.")
        with st.expander("Show unmatched lines"):
            st.dataframe(unmatched_df)
else:
    st.caption("Upload your Promised Payments PDF to begin.")
st.sidebar.info("This tool converts a Promised Payments Report PDF into a structured CSV format. It skips rows with statuses 'Paid In Full' or 'Settled In Full' and highlights unmatched lines for review.")
st.sidebar.markdown("### How to Use")
st.sidebar.markdown("""
1. Upload your Promised Payments Report PDF using the file uploader.
2. Review the parsed data in the table.
3. Download the structured CSV file using the download button.
4. Check the skipped and unmatched lines for any issues.
""")