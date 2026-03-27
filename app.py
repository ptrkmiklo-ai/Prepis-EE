import streamlit as st
from utils import get_template_path
from pdf_generator import generate_pdf, dynamic_fields_from_csv
from data_loader import get_people_list
import os

st.set_page_config(page_title="Prepis elektriny", layout="centered")

st.title("⚡ Prepis elektrickej energie")

provider = st.selectbox("Dodávateľ:", ["ZSE", "SSE"])

people = get_people_list()
person_display = st.selectbox("Vyberte osobu:", list(people.keys()))
person_data = people[person_display]

if st.button("Vygenerovať PDF"):
    template_path = get_template_path(provider)
    fields = dynamic_fields_from_csv(person_data)

    output = "/data/out/files/prepis.pdf"
    generate_pdf(fields, template_path, output)

    st.success("PDF bolo vygenerované ✔")

    with open(output, "rb") as f:
        st.download_button(
            label="📄 Stiahnuť PDF",
            data=f.read(),
            file_name="prepis.pdf",
            mime="application/pdf"
        )
``
