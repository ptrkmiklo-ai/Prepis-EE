import streamlit as st
from utils import get_template_path
from pdf_generator import generate_pdf
from snowflake.connector import connect
import os

st.set_page_config(page_title="Prepis elektriny", layout="centered")

st.title("⚡ Prepis elektrickej energie")

# --- Snowflake pripojenie ---
def get_snowflake_connection():
    return connect(
        user=os.environ["SF_USER"],
        password=os.environ["SF_PASSWORD"],
        account=os.environ["SF_ACCOUNT"],
        warehouse=os.environ["SF_WAREHOUSE"],
        database=os.environ["SF_DATABASE"],
        schema=os.environ["SF_SCHEMA"]
    )

# --- načítanie osôb ---
@st.cache_data
def load_people():
    conn = get_snowflake_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT ID, MENO, PRIEZVISKO
        FROM NAJOMCOVIA
        ORDER BY PRIEZVISKO, MENO;
    """)
    rows = cur.fetchall()
    conn.close()
    return {f"{r[2]} {r[1]} (ID: {r[0]})": r[0] for r in rows}

# --- UI ---
provider = st.selectbox("Dodávateľ:", ["ZSE", "SSE"])

people = load_people()
person_display = st.selectbox("Vyberte osobu:", list(people.keys()))
person_id = people[person_display]

if st.button("Vygenerovať PDF"):
    conn = get_snowflake_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM NAJOMCOVIA WHERE ID=%s", (person_id,))
    row = cur.fetchone()
    columns = [c[0] for c in cur.description]
    person_data = dict(zip(columns, row))
    conn.close()

    template_path = get_template_path(provider)

    output_path = "/data/out/files/prepis.pdf"
    generate_pdf(person_data, template_path, output_path)

    st.success("PDF bolo úspešne vygenerované ✔")

    with open(output_path, "rb") as f:
        st.download_button(
            label="📄 Stiahnuť PDF",
            data=f.read(),
            file_name="prepis.pdf",
            mime="application/pdf"
        )
