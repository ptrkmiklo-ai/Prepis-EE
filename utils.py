import os

TEMPLATE_DIR = "/app/templates"

def get_template_path():
    path = os.path.join(TEMPLATE_DIR, "zse.pdf")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Šablóna ZSE neexistuje: {path}")
    return path
