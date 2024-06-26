from bs4 import BeautifulSoup


def jinja2_filter_has_text(value):
    if not isinstance(value, str):
        return False

    soup = BeautifulSoup(value, "html.parser")
    text = soup.get_text().strip()

    return bool(text)
