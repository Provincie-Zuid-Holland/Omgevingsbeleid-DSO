from bs4 import BeautifulSoup


def calculate_columns(row):
    columns = 0
    for cell in row.find_all(["td", "th"], recursive=False):
        colspan = cell.get("colspan")
        columns += int(colspan) if colspan else 1
    return columns


def middleware_enrich_table(html):
    soup = BeautifulSoup(html, "html.parser")

    for table in soup.find_all("table"):
        first_row = table.find("tr")
        if not first_row:
            continue

        # Set the column count as am attribute in the table
        # That makes it easier for the tekst parser to build the colspec
        max_columns = calculate_columns(first_row)
        table["data-columns"] = str(max_columns)

        # This will move the first row into a thead if that is needed
        if not table.thead:
            first_row = table.find("tr")
            if first_row and all(cell.name == "th" for cell in first_row.find_all(recursive=False)):
                thead = soup.new_tag("thead")
                thead.append(first_row.extract())
                table.insert(0, thead)

    return str(soup)
