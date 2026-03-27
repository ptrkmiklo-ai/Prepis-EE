import os

TEMPLATE_DIR = "/app/templates"

def get_template_path(provider: str, form_type: str = None) -> str:
    """
    provider: 'ZSE', 'SSE'
    form_type: optional (e.g. 'DOMACNOST', 'FIRMA')
    """

    provider = provider.upper().strip()

    # mapovanie základných šablón
    base_files = {
        "ZSE": "ZSE.pdf",
        "SSE": "SSE.pdf"
    }

    # 1) ak vieme, že máme len 1 šablónu na dodávateľa
    if provider in base_files:
        path = os.path.join(TEMPLATE_DIR, base_files[provider])
        if os.path.exists(path):
            return path
        raise FileNotFoundError(f"Šablóna pre {provider} neexistuje: {path}")

    # 2) fallback
    raise ValueError(f"Nepodporovaný dodávateľ: {provider}")
