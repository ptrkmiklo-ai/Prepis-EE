import os
import fitz
from PyPDF2 import PdfReader, PdfWriter

def generate_pdf(person_data, template_path, output_path):

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
        "Za_Odberatela_Meno_priezvisko_povodneho_odbetratela_13": "Lucia Volleková, splnomocnenec",
    }

    dynamic_fields = {
        "Meno a priezvisko_5": person_data["NAME"],
        "Datum narodenia_5": person_data["RC"],
        "Telefon_5": person_data["MOBIL"],
        "Email_5": person_data["EMAIL"],
        "Ulica_5": person_data["ADDRESS"],
        "Obec_5": person_data["CITY"],
        "PSC_5": person_data["ZIP"],
        "Ulica_7": person_data["ADDRESS"],
        "Obec_7": person_data["CITY"],
        "PSC_7": person_data["ZIP"],
        "Cislo_elektromera_8": person_data["OP"],
        "Cislo or_5": "",
        "Cislo or_3": "",
    }

    reader = PdfReader(template_path)
    writer = PdfWriter()
    for page in reader.pages:
        writer.add_page(page)

    field_values = {**constant_fields, **dynamic_fields}
    for page in writer.pages:
        writer.update_page_form_field_values(page, field_values)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        writer.write(f)

    doc = fitz.open(output_path)

    coords_X = {1: [(29, 640), (29, 687)]}
    coords_email = {3: [(248, 187)]}

    for page_num, coords in coords_X.items():
        page = doc[page_num - 1]
        for x, y in coords:
            page.insert_text((x, y), "X")

    for page_num, coords in coords_email.items():
        page = doc[page_num - 1]
        for x, y in coords:
            page.insert_text((x, y), "energie@dostupnydomov.sk")

    doc.save(output_path)
    doc.close()

    return output_path
