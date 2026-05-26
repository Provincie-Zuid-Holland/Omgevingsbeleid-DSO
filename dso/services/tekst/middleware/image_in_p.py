from typing import Tuple

from lxml import html


def middleware_image_in_p(html_content: str) -> str:
    modified_html, modified = _process_html(html_content)
    while modified:
        modified_html, modified = _process_html(modified_html)

    return modified_html


def _process_html(html_content: str) -> Tuple[str, bool]:
    # Wrap the input in a <div> to ensure a single root
    wrapped_html: str = f"<div>{html_content}</div>"

    tree = html.fromstring(wrapped_html)
    modified: bool = False

    for element in tree.xpath(".//p"):
        for child in list(element):
            if child.tag == "img":
                new_p_tag = html.Element("p")

                if child.tail is not None:
                    new_p_tag.text = (new_p_tag.text or "") + child.tail
                    child.tail = None

                next_sibling = child.getnext()
                while next_sibling is not None:
                    new_p_tag.append(next_sibling)
                    next_sibling = next_sibling.getnext()

                element.addnext(new_p_tag)
                element.addnext(child)
                modified = True
                # Break to handle only the first <img> in each <p>
                break

    modified_html: str = html.tostring(tree, pretty_print=True, encoding="unicode")

    modified_html: str = modified_html.replace("<div>", "", 1)
    modified_html: str = modified_html.rsplit("</div>", 1)[0]

    return modified_html, modified
