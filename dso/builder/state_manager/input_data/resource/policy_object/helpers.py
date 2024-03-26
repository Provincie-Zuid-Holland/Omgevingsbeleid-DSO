from typing import Optional


def visie_algemeen_as_html(o: dict, heading_number: Optional[int] = None) -> str:
    heading_number_attr: str = ""
    if heading_number is not None:
        heading_number_attr = f' data-nummer="{heading_number}"'
    html = f"""<h1{heading_number_attr}>{o['Title']}</h1>{o['Description']}"""
    return html
