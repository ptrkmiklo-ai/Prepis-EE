import streamlit as st
from data_loader import get_people_list
from utils import get_template_path
from pdf_generator import generate_pdf
import os

st.set_page_config(page_title="Prepis elektriny ZSE", layout="centered")
st.title("⚡ Prepis elektrickej energie – ZSE")

# Načítanie ľudí z adresar.csv
people = get_people_list()

if not people:
    st.error("adresar.csv je prázdny alebo obsahuje nesprávne dáta.")
else:
    # Zobraziť dropdown s menami
    person_display = st.selectbox("Vyberte osobu:", list(people.keys()))
    person_data = people[person_display]

    if st.button("Vygenerovať PDF"):
        try:
            template = get_template_path()
            output = "/data/out/files/zse_prepis.pdf"

            generate_pdf(person_data, template, output)

            st.success("PDF bolo úspešne vygenerované ✔")

            with open(output, "rb") as f:
                st.download_button(
                    label="📄 Stiahnuť PDF",
                    data=f.read(),
                    file_name="zse_prepis.pdf",
                    mime="application/pdf"
                )
        except Exception as e:
            st.error(f"Chyba pri generovaní PDF: {e}")
``
