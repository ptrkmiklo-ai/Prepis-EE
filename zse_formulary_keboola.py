import os
import fitz
import logging
import warnings
from PyPDF2 import PdfReader, PdfWriter
import pandas as pd

warnings.filterwarnings("ignore")
logging.getLogger("PyPDF2").setLevel(logging.ERROR)

FORBIDDEN_CHARS = '\\/?:*"><|'

def make_safe_filename(name: str) -> str:
    return "".join("_" if c in FORBIDDEN_CHARS else c for c in name).strip()[:120]



ADR_PATH = "/data/in/tables/adresar.csv"

def load_person_from_adresar(person_id: str):
    df = pd.read_csv(ADR_PATH)

    # predpokladáme, že máš stĺpec ID
    row = df[df["ID"] == person_id]

    if row.empty:
        raise ValueError("Osoba sa nenašla v tabuľke Adresar.")

    return row.iloc[0].to_dict()

    
    cur = conn.cursor()
    cur.execute("""
        SELECT *
        FROM NAJOMCOVIA
        WHERE ID = %s
    """, (person_id,))
    
    row = cur.fetchone()
    columns = [col[0] for col in cur.description]
    conn.close()
    
    if not row:
        raise ValueError("Nájomca neexistuje v Snowflake.")
    
    return dict(zip(columns, row))


def generate_pdf(person_data: dict, template_path: str, output_pdf: str):
    """Vytvorenie PDF podľa tvojej šablóny a existujúcej logiky."""

    # ---- KONŠTANTY (ponechané z tvojho skriptu) ----
    constant_fields = {
        "Nazov_Obchodne_meno_1": "Dostupný Domov j.s.a.",
        "Cislo_obchodneho_partnera_1": "5750395461",
        "Ulica_2": "Farská",
        "Obec_2": "Nitra",
        "Cislo or_2": "48",
        "PSC_2": "949 01",
        "E-mail_2": "dostupnydomov@dostupnydomov.sk",
        "Telefon_2": "0903 462 307",
        "Meno_priezvisko_funkcia_zastupeny_2_1": "Lucia Volleková, splnomocnenec",
        "Telefon_zastupeny_2_1": "0903 462 307",
        "Email_na_elektronicku_fakturu_4": "dostupnydomov@dostupnydomov.sk",
        "EE_IBAN_4": "SK29 0900 0000 0051 6938 2166",
        "Za_Odberatela_Meno_priezvisko_povodneho_odbetratela_13": "Lucia Volleková, splnomocnenec"
    }

    # ---- MAPOVANIE POLÍ Z SNOWFLAKE ----
    # tu môžeš zachovať tvoje názvy stĺpcov
    dynamic_fields = {
        "Meno a priezvisko_5": person_data["MENO"],
        "Datum narodenia_5": person_data["DATUM_NAR"],
        "Ulica_5": person_data["ULICA"],
        "Obec_5": person_data["OBEC"],
        "PSC_5": person_data["PSC"],
        "Telefon_5": person_data["TELEFON"],
        "Email_5": person_data["EMAIL"],
        "EIC_odberneho_miesta_3": person_data["EIC"],
        "Cislo miesta spotreby_3": person_data["MIS_SPOTREBY"]
    }

    # ---- načítanie šablóny ----
    reader = PdfReader(template_path)
    writer = PdfWriter()
    
    for page in reader.pages:
        writer.add_page(page)

    # ---- vkladanie do PDF form fields ----
    field_values = {**constant_fields, **dynamic_fields}

    for page in writer.pages:
        writer.update_page_form_field_values(page, field_values)

    # ---- uloženie medzisúboru ----
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    with open(output_pdf, "wb") as f:
        writer.write(f)

    # ---- doplnenie „X“ a emailov cez PyMuPDF ----
    doc = fitz.open(output_pdf)

    coords_X = {1: [(29, 640), (29, 687)]}
    coords_email = {3: [(248, 187)]}

    for page_num, coords_list in coords_X.items():
        page = doc[page_num - 1]
        for x, y in coords_list:
            page.insert_text((x, y), "X")

    for page_num, coords_list in coords_email.items():
        page = doc[page_num - 1]
        for x, y in coords_list:
            page.insert_text((x, y), "energie@dostupnydomov.sk")

    doc.save(output_pdf)
    doc.close()

    return output_pdf
