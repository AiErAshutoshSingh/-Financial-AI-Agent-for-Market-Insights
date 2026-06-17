import streamlit as st
from reportlab.pdfgen import canvas

st.title("📄 Generate PDF Report")

if st.button("Generate Report"):

    pdf_file = "finance_report.pdf"

    c = canvas.Canvas(pdf_file)

    c.drawString(
        100,
        750,
        "AI Finance Report"
    )

    c.drawString(
        100,
        720,
        "Generated Successfully"
    )

    c.save()

    with open(pdf_file,"rb") as f:

        st.download_button(
            "Download PDF",
            f,
            file_name=pdf_file
        )