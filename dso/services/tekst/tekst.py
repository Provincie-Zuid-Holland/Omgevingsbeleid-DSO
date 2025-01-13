import re
from abc import ABCMeta, abstractmethod
from typing import Any, Dict, List, Optional, Type, TypeAlias, Union

from bs4 import BeautifulSoup, CData, Comment, Declaration, Doctype, NavigableString, ProcessingInstruction, Tag

from .lijst import LijstType, LijstTypeOrdered, LijstTypeUnordered, NumberingStrategy, numbering_factory

object_code_regex = r"\[OBJECT-CODE:(.*?)\]"
gebied_code_regex = r"\[GEBIED-CODE:(.*?)\]"


def extract_object_code(text: str) -> Optional[str]:
    matched = re.search(object_code_regex, text)
    if not matched:
        return None
    result = matched.group(1)
    return result


def extract_gebied_code(text: str) -> Optional[str]:
    matched = re.search(gebied_code_regex, text)
    if not matched:
        return None
    result = matched.group(1)
    return result


class AsXmlTrait(metaclass=ABCMeta):
    @abstractmethod
    def as_xml(self, soup: BeautifulSoup) -> Union[Tag, str]:
        pass


LeftoverTag: TypeAlias = Optional[Tag]


class IsEmptyTrait(metaclass=ABCMeta):
    @abstractmethod
    def is_empty(self) -> bool:
        pass


class Element(AsXmlTrait, metaclass=ABCMeta):
    def consume_children(self, children: List[Any]):
        for element in children:
            if isinstance(element, Comment):
                self.consume_comment(element)
            elif isinstance(element, NavigableString):
                self.consume_string(element)
            elif isinstance(element, Doctype):
                raise NotImplementedError("Doctype", element)
            elif isinstance(element, CData):
                raise NotImplementedError("CData", element)
            elif isinstance(element, ProcessingInstruction):
                raise NotImplementedError("ProcessingInstruction", element)
            elif isinstance(element, Declaration):
                raise NotImplementedError("Declaration", element)
            elif isinstance(element, Tag):
                self.consume_tag(element)
            else:
                raise Exception("Unknown type", element)

    @abstractmethod
    def consume_tag(self, tag: Tag) -> LeftoverTag:
        pass

    @abstractmethod
    def consume_string(self, string: NavigableString):
        pass

    def consume_comment(self, comment: Comment) -> LeftoverTag:
        raise NotImplementedError("Comment", comment)


class ElementGenerator(metaclass=ABCMeta):
    def can_consume_tag(self, tag: Tag) -> bool:
        pass

    def generate(self, tag: Tag, context: dict = {}) -> Element:
        pass


class SimpleElement(Element, metaclass=ABCMeta):
    element_generators: List[ElementGenerator] = []

    def __init__(self, xml_tag_name: str = "", xml_tag_attrs: Dict[str, str] = {}):
        self.contents: List[Union[Element, str]] = []
        self.xml_tag_name: str = xml_tag_name
        self.xml_tag_attrs: Dict[str, str] = xml_tag_attrs

    def consume_tag(self, tag: Tag) -> LeftoverTag:
        for element_generator in self.element_generators:
            if not element_generator.can_consume_tag(tag):
                continue
            content: Element = element_generator.generate(
                tag=tag,
                context=self._get_generate_context(),
            )
            content.consume_children(tag.children)
            self.contents.append(content)
            return None
        return tag

    def consume_string(self, string: NavigableString):
        self.contents.append(str(string))

    def as_xml(
        self,
        soup: BeautifulSoup,
        tag_name_overwrite: Optional[str] = None,
        tag_attrs_overwrite: Optional[Dict[str, str]] = None,
    ) -> Union[Tag, str]:
        tag_name: str = tag_name_overwrite if tag_name_overwrite is not None else self.xml_tag_name
        tag: Tag = soup.new_tag(tag_name)
        tag.attrs = tag_attrs_overwrite if tag_attrs_overwrite is not None else self.xml_tag_attrs

        for content in self.contents:
            if hasattr(content, "as_xml"):
                child = content.as_xml(soup)
                if child != "":
                    tag.append(child)
            elif isinstance(content, str):
                tag.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")

        return tag

    def _get_generate_context(self) -> dict:
        return {}


class SimpleGenerator(ElementGenerator):
    def __init__(self, tag_name: str, class_type: Type[SimpleElement]):
        self._tag_name: str = tag_name
        self._class_type: Type[SimpleElement] = class_type

    def can_consume_tag(self, tag: Tag) -> bool:
        return tag.name == self._tag_name

    def generate(self, tag: Tag, context: dict = {}) -> Element:
        element = self._class_type(tag)
        return element


class OrderedLijstGenerator(ElementGenerator):
    def can_consume_tag(self, tag: Tag) -> bool:
        return tag.name == "ol"

    def generate(self, tag: Tag, context: dict = {}) -> Element:
        current_strategy: Optional[NumberingStrategy] = context.get("current_strategy", None)
        next_strategy: NumberingStrategy = numbering_factory.get_next(current_strategy)
        element = Lijst(
            tag=tag,
            lijst_type=LijstTypeOrdered(next_strategy),
        )
        return element


class UnorderedLijstGenerator(ElementGenerator):
    def can_consume_tag(self, tag: Tag) -> bool:
        return tag.name == "ul"

    def generate(self, tag: Tag, context: dict = {}) -> Element:
        element = Lijst(
            tag=tag,
            lijst_type=LijstTypeUnordered(),
        )
        return element


class LiGenerator(ElementGenerator):
    def can_consume_tag(self, tag: Tag) -> bool:
        return tag.name == "li"

    def generate(self, tag: Tag, context: dict = {}) -> Element:
        lijst_type: Optional[LijstType] = context.get("lijst_type", None)
        if lijst_type is None:
            raise RuntimeError("Missing required context LijstType to create a Li")
        idx: Optional[int] = context.get("idx", None)
        if idx is None:
            raise RuntimeError("Missing required context idx to create a Li")
        element = Li(tag, lijst_type, idx)
        return element


class RefGenerator(ElementGenerator):
    def can_consume_tag(self, tag: Tag) -> bool:
        return tag.name == "a"

    def generate(self, tag: Tag, context: dict = {}) -> Element:
        hint_type: Optional[str] = tag.get("data-hint-type", None)
        if hint_type == "gebiedsaanwijzing":
            return GebiedsaanwijzingRef(tag)

        if hint_type == "document":
            return DocumentRef(tag)

        if hint_type == "object":
            return TekstObjectRef(tag)

        return ExtRef(tag)


class I(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(xml_tag_name="i")


class B(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(xml_tag_name="b")


class U(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(xml_tag_name="u")


class Sub(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(xml_tag_name="sub")


class Sup(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(xml_tag_name="sup")


class Strong(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(xml_tag_name="strong")


class TussenKop(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(xml_tag_name="Tussenkop")


class Al(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(xml_tag_name="Al")

    def as_xml(self, soup: BeautifulSoup, tag_name_overwrite: Optional[str] = None) -> Union[Tag, str]:
        if self._is_empty():
            return ""

        return SimpleElement.as_xml(self, soup=soup, tag_name_overwrite=tag_name_overwrite)

    def _is_empty(self):
        if not self.contents:
            return True

        for content in self.contents:
            if isinstance(content, str):
                if content.strip() != "":
                    return False
            elif not isinstance(content, Br):
                return False
        return True


class Br(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(xml_tag_name="br")


class Figuur(SimpleElement):
    src_pattern = r"^\[ASSET:(.{36})\]$"

    def __init__(self, tag: Optional[Tag] = None):
        super().__init__()
        self._asset_uuid: str = ""

        src: str = tag.attrs.get("src", "")
        if not src:
            raise RuntimeError("Missing required attribute src for image")
        src_match = re.match(self.src_pattern, src)
        if not src_match:
            raise RuntimeError("Wrong format for image src")
        self._asset_uuid = src_match.group(1)

    def as_xml(self, soup: BeautifulSoup, tag_name_overwrite: Optional[str] = None) -> Union[Tag, str]:
        figuur: Tag = soup.new_tag("Figuur")
        illustratie: Tag = soup.new_tag("Illustratie")
        illustratie.attrs = {
            "data-hint-asset-uuid": self._asset_uuid,
        }

        figuur.append(illustratie)
        return figuur


class ExtRef(SimpleElement):
    AKN_PATTERN = r"^/akn/"

    def __init__(self, tag: Optional[Tag] = None):
        super().__init__()
        self.href: str = tag.get("href")
        self.soort: str = "URL"
        if re.match(self.AKN_PATTERN, self.href):
            self.soort = "AKN"

    def as_xml(self, soup: BeautifulSoup, tag_name_overwrite: Optional[str] = None) -> Union[Tag, str]:
        result = SimpleElement.as_xml(
            self,
            soup=soup,
            tag_name_overwrite="ExtRef",
            tag_attrs_overwrite={
                "ref": self.href,
                "soort": self.soort,
            },
        )
        return result


class TekstObjectRef(SimpleElement):
    def __init__(self, tag: Tag):
        super().__init__()
        self.object_code: str = tag["data-hint-value"]

    def as_xml(self, soup: BeautifulSoup, tag_name_overwrite: Optional[str] = None) -> Union[Tag, str]:
        result = SimpleElement.as_xml(
            self,
            soup=soup,
            tag_name_overwrite="IntRef",
            tag_attrs_overwrite={
                "ref": "",
                "data-hint-type": "object",
                "data-hint-target-object-code": self.object_code,
            },
        )
        return result


class DocumentRef(SimpleElement):
    """
    Example input:
    <a href="/join/id/regdata/pv28/2024/at-14-4-28/nld@2024-11-14;1" data-hint-document-code="document-1">Title</a>

    Example output:
    <ExtIoRef ref="" data-hint-document-code="document-1">Title</ExtIoRef>

    The `ref` will be set later with help of the data-hint-document-code
    """

    def __init__(self, tag: Tag):
        super().__init__()
        self._document_code: Optional[str] = tag.get("data-hint-document-code", None)

    def as_xml(self, soup: BeautifulSoup, tag_name_overwrite: Optional[str] = None) -> Union[Tag, str]:
        result = SimpleElement.as_xml(
            self,
            soup=soup,
            tag_name_overwrite="IntIoRef",
            tag_attrs_overwrite={
                "ref": "",
                "data-hint-type": "document",
                "data-hint-document-code": self._document_code,
            },
        )
        return result


class GebiedsaanwijzingRef(SimpleElement):
    def __init__(self, tag: Tag):
        super().__init__()
        self.href: str = tag.get("href")
        self.type: Optional[str] = tag.get("data-hint-gebiedsaanwijzingtype", None)
        self.gebiedengroep: Optional[str] = tag.get("data-hint-gebiedengroep", None)
        self.gebiedsaanwijzing: Optional[str] = tag.get("data-hint-locatie", None)

    def as_xml(self, soup: BeautifulSoup, tag_name_overwrite: Optional[str] = None) -> Union[Tag, str]:
        result = SimpleElement.as_xml(
            self,
            soup=soup,
            tag_name_overwrite="IntIoRef",
            tag_attrs_overwrite={
                "ref": self.href,
                "data-hint-type": "gebiedsaanwijzing",
                "data-hint-gebiedsaanwijzingtype": self.type,
                "data-hint-gebiedengroep": self.gebiedengroep,
                "data-hint-locatie": self.gebiedsaanwijzing,
            },
        )
        return result


class Kop(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__()
        self.nummer: Optional[str] = None

        if tag is not None:
            self.nummer = tag.get("data-nummer", None)

    def as_xml(self, soup: BeautifulSoup) -> Union[Tag, str]:
        kop: Tag = soup.new_tag("Kop")

        if self.nummer is not None:
            nummer: Tag = soup.new_tag("Nummer")
            nummer.append(str(self.nummer))
            kop.append(nummer)

        opschrift = SimpleElement.as_xml(self, soup=soup, tag_name_overwrite="Opschrift")
        kop.append(opschrift)

        return kop


class Inhoud(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(xml_tag_name="Inhoud")


# td
class Entry(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(
            xml_tag_name="entry",
            xml_tag_attrs={
                "align": "left",
                "valign": "top",
            },
        )

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) == 0:
            return

        al: Al = Al(tag=None)
        al.consume_string(string)
        self.contents.append(al)


# tr
class Row(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(xml_tag_name="row")

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) != 0:
            raise RuntimeError(f"Can not write plain text to Row. Trying to write: {raw}")


class Tbody(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(
            xml_tag_name="tbody",
            xml_tag_attrs={
                "valign": "top",
            },
        )

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) != 0:
            raise RuntimeError(f"Can not write plain text to Tbody. Trying to write: {raw}")


class Thead(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(
            xml_tag_name="thead",
            xml_tag_attrs={
                "valign": "top",
            },
        )

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) != 0:
            raise RuntimeError(f"Can not write plain text to Thead. Trying to write: {raw}")


class Table(Element):
    def __init__(self, tag: Optional[Tag] = None):
        self.columns: int = int(tag.attrs.get("data-columns"))
        self.thead: Optional[Thead] = None
        self.tbody: Optional[Tbody] = None

    def consume_tag(self, tag: Tag) -> LeftoverTag:
        if tag.name == "thead":
            if self.thead is not None:
                raise RuntimeError("Multiple thead are not supported")
            self.thead = Thead(tag)
            self.thead.consume_children(tag.children)
            return None
        if tag.name == "tbody":
            if self.tbody is not None:
                raise RuntimeError("Multiple tbody are not supported")
            self.tbody = Tbody(tag)
            self.tbody.consume_children(tag.children)
            return None

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) == 0:
            return
        raise RuntimeError(f"Consume string not implemented for Table")

    def as_xml(self, soup: BeautifulSoup) -> Union[Tag, str]:
        table: Tag = soup.new_tag("table")
        tgroup: Tag = soup.new_tag("tgroup")
        tgroup["cols"] = self.columns
        tgroup["align"] = "left"

        for i in range(1, self.columns + 1):
            colspec: Tag = soup.new_tag("colspec")
            colspec["colname"] = f"col{i}"
            colspec["colnum"] = f"{i}"
            tgroup.append(colspec)

        if self.thead is not None:
            thead = self.thead.as_xml(soup)
            tgroup.append(thead)

        if self.tbody is not None:
            tbody = self.tbody.as_xml(soup)
            tgroup.append(tbody)

        table.append(tgroup)
        return table


class Li(SimpleElement):
    def __init__(self, tag: Optional[Tag], lijst_type: LijstType, idx: int):
        super().__init__()
        self.lijst_type: LijstType = lijst_type
        self.idx: int = idx

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) == 0:
            return

        al: Al = Al(tag=None)
        al.consume_string(string)
        self.contents.append(al)

    def as_xml(self, soup: BeautifulSoup) -> Union[Tag, str]:
        tag_li: Tag = soup.new_tag("Li")
        if self.lijst_type.has_number():
            nummer: str = self.lijst_type.get_number(self.idx)

            tag_li_nummer: Tag = soup.new_tag("LiNummer")
            tag_li_nummer.append(nummer)

            tag_li.append(tag_li_nummer)

        for content in self.contents:
            if hasattr(content, "as_xml"):
                child = content.as_xml(soup)
                tag_li.append(child)
            elif isinstance(content, str):
                tag_li.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")

        return tag_li

    def _get_generate_context(self) -> dict:
        current_strategy: Optional[NumberingStrategy] = self.lijst_type.get_numbering_strategy()
        return {
            "current_strategy": current_strategy,
        }


class Lijst(SimpleElement):
    def __init__(self, tag: Optional[Tag], lijst_type: LijstType):
        super().__init__()
        self.lijst_type: LijstType = lijst_type

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) != 0:
            raise RuntimeError(f"Can not write plain text to Lijst. Trying to write: {raw}")

    def as_xml(self, soup: BeautifulSoup) -> Union[Tag, str]:
        attributes: dict = {"type": self.lijst_type.get_type()}
        tag: Tag = soup.new_tag("Lijst", **attributes)
        for content in self.contents:
            if hasattr(content, "as_xml"):
                child = content.as_xml(soup)
                tag.append(child)
            elif isinstance(content, str):
                tag.append(content)
            else:
                raise RuntimeError("Can not convert child to xml")

        return tag

    def _get_generate_context(self) -> dict:
        return {
            "lijst_type": self.lijst_type,
            "idx": len(self.contents) + 1,
        }


class Divisietekst(Element):
    def __init__(self, tag: Optional[Tag] = None):
        self.kop: Optional[Kop] = None
        self.inhoud: Optional[Inhoud] = None
        self.wid_code: Optional[str] = None
        self.object_code: Optional[str] = None

        if tag is not None:
            self.wid_code = tag.get("data-hint-wid-code", None)
            self.object_code = tag.get("data-hint-object-code", None)

    def consume_tag(self, tag: Tag) -> LeftoverTag:
        # A div requires a new Divisie which a Divisietekst can not create
        if tag.name == "div":
            return tag

        # Headings will be send to the Kop
        if tag.name in ["h1", "h2"]:
            if self.kop is not None:
                return tag
            kop = Kop(tag)
            kop.consume_children(tag.children)
            self.kop = kop
            return None

        # Any other tags will just be send in a Inhoud
        inhoud: Inhoud = self._get_inhoud()
        leftoverTag: LeftoverTag = inhoud.consume_tag(tag)

        return leftoverTag

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) == 0:
            return
        raise RuntimeError(f"Consume string not implemented for Divisietekst for code {self.object_code}")

    def consume_comment(self, comment: Comment) -> LeftoverTag:
        """
        Divisietekst template comments:
            - [OBJECT-CODE:objecttype-123]
        """
        object_code: Optional[str] = extract_object_code(str(comment))
        if object_code is not None:
            self.object_code = object_code

        return None

    def _get_inhoud(self) -> Inhoud:
        if self.inhoud is None:
            self.inhoud = Inhoud(tag=None)

        return self.inhoud

    def as_xml(self, soup: BeautifulSoup) -> Union[Tag, str]:
        tag_divisietekst: Tag = soup.new_tag("Divisietekst")
        wid_code = self.wid_code or self.object_code

        tag_divisietekst.attrs = {
            **({"data-hint-wid-code": wid_code} if wid_code else {}),
            **({"data-hint-object-code": self.object_code} if self.object_code else {}),
        }

        if self.kop is not None:
            tag_kop: Tag = self.kop.as_xml(soup)
            tag_divisietekst.append(tag_kop)

        if self.inhoud is not None:
            tag_inhoud: Tag = self.inhoud.as_xml(soup)
            tag_divisietekst.append(tag_inhoud)

        return tag_divisietekst


class Divisie(Element):
    def __init__(self, tag: Optional[Tag] = None):
        self.kop: Optional[Kop] = None
        self.contents: List[Union["Divisie", Divisietekst]] = []
        self.wid_code = tag.get("data-hint-wid-code", None)
        self.object_code = tag.get("data-hint-object-code", None)

    def consume_tag(self, tag: Tag) -> LeftoverTag:
        while True:
            leftoverTag = self._try_consume_tag(tag)
            if leftoverTag is None:
                return None

    def _try_consume_tag(self, tag: Tag) -> LeftoverTag:
        # Headings will be send to the Kop
        if tag.name in ["h1", "h2", "h3", "h4"]:
            if self.kop is not None:
                # If we already have a title and we need a title
                # Then we create a new Divisie or Divisietekst based on the title level
                # and then let that new component consume the title
                # if tag.name in ["h1", "h2"]:
                #     content: Divisie = Divisie()
                #     self.contents.append(content)
                #     leftover = content.consume_tag(tag)
                #     return leftover
                # else:
                content: Divisietekst = Divisietekst()
                self.contents.append(content)
                leftover = content.consume_tag(tag)
                return leftover

            if self.contents:
                # We cant set the heading if we already have content.
                # That would render the text out of order
                # In this case we just pass allong to the divisie tekst
                # content: Divisietekst = self._get_active_divisietekst()
                # leftover = content.consume_tag(tag)
                # @note: scrapped above, i think we should create a new divisietekst in this case
                content: Divisietekst = Divisietekst()
                self.contents.append(content)
                leftover = content.consume_tag(tag)
                return leftover

            kop = Kop(tag)
            kop.consume_children(tag.children)
            self.kop = kop
            return None

        # If the tag is a div then we will create a new Divisie
        elif tag.name == "div":
            if tag.attrs.get("data-hint-element", None) == "divisietekst":
                content: Divisietekst = Divisietekst()
                self.contents.append(content)
                leftover = content.consume_children(tag.children)
                return leftover
            else:
                content: Divisie = Divisie(tag)
                self.contents.append(content)
                leftover_maybe = content.consume_children(tag.children)
                if leftover_maybe is not None:
                    a = True
                return None

        # Else we will let the last Divisietekst consume the tag
        else:
            # If we do not have an "active Divisietekst" then we will create one
            content: Divisietekst = self._get_active_divisietekst()
            leftover = content.consume_tag(tag)
            return leftover

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) == 0:
            return
        raise RuntimeError(f"Consume string not implemented for Divisie. For code: {self.object_code}")

    def consume_comment(self, comment: Comment) -> LeftoverTag:
        """
        Divisie template comments:
            - [OBJECT-CODE:objecttype-123]
        """
        object_code: Optional[str] = extract_object_code(str(comment))
        if object_code is not None:
            self.object_code = object_code

        return None

    def _get_active_divisietekst(self) -> Divisietekst:
        # No content at all
        if not len(self.contents):
            content: Divisietekst = Divisietekst()
            self.contents.append(content)

        # Last content is not a divisietekst
        last_content = self.contents[-1]
        if not isinstance(last_content, Divisietekst):
            content: Divisietekst = Divisietekst()
            self.contents.append(content)

        # Return the last which is now forced to be a Divisietekst
        return self.contents[-1]

    def as_xml(self, soup: BeautifulSoup) -> Union[Tag, str]:
        tag_divisie: Tag = soup.new_tag("Divisie")
        wid_code = self.wid_code or self.object_code

        tag_divisie.attrs = {
            **({"data-hint-wid-code": wid_code} if wid_code else {}),
            **({"data-hint-object-code": self.object_code} if self.object_code else {}),
        }

        if self.kop is not None:
            tag_kop: Tag = self.kop.as_xml(soup)
            tag_divisie.append(tag_kop)

        # Loop through contents and append them to the Divisie tag
        for content in self.contents:
            if hasattr(content, "as_xml"):
                child = content.as_xml(soup)
                tag_divisie.append(child)
            elif isinstance(content, str):
                tag_divisie.append(content)
            else:
                raise RuntimeError("Cannot convert child to XML")

        return tag_divisie


class Lichaam(SimpleElement):
    def __init__(self, tag: Optional[Tag] = None):
        super().__init__(
            xml_tag_name="Lichaam",
            xml_tag_attrs={
                # @todo: Should be done by the wid service
                "eId": "body",
                "wId": "body",
            },
        )

    def consume_tag(self, tag: Tag) -> LeftoverTag:
        if tag.name not in ["div", "object"]:
            raise RuntimeError("Lichaam only expects 'div' and 'object' as elements")

        if tag.attrs.get("data-hint-element", None) == "divisietekst":
            content: Element = Divisietekst(tag)
        else:
            content: Element = Divisie(tag)

        content.consume_children(tag.children)
        self.contents.append(content)
        return None

    def consume_string(self, string: NavigableString):
        raw: str = str(string).strip()
        if len(raw) != 0:
            raise RuntimeError(f"Can not write plain text to Lijst. Trying to write: {raw}")


element_i_handler = SimpleGenerator("i", I)
element_em_handler = SimpleGenerator("em", I)
element_b_handler = SimpleGenerator("b", B)
element_u_handler = SimpleGenerator("u", U)
element_sub_handler = SimpleGenerator("sub", Sub)
element_sup_handler = SimpleGenerator("sup", Sup)
element_strong_handler = SimpleGenerator("strong", Strong)
element_p_handler = SimpleGenerator("p", Al)
element_ul_handler = UnorderedLijstGenerator()
element_ol_handler = OrderedLijstGenerator()
element_li_handler = LiGenerator()
element_br_handler = SimpleGenerator("br", Br)
element_div_handler = SimpleGenerator("div", Divisie)
element_img_handler = SimpleGenerator("img", Figuur)
element_td_handler = SimpleGenerator("td", Entry)
element_th_handler = SimpleGenerator("th", Entry)
element_tr_handler = SimpleGenerator("tr", Row)
element_tbody_handler = SimpleGenerator("tbody", Tbody)
element_thead_handler = SimpleGenerator("thead", Thead)
element_table_handler = SimpleGenerator("table", Table)
element_h1_tussenkop_handler = SimpleGenerator("h1", TussenKop)
element_h2_tussenkop_handler = SimpleGenerator("h2", TussenKop)
element_h3_tussenkop_handler = SimpleGenerator("h3", TussenKop)
element_h4_tussenkop_handler = SimpleGenerator("h4", TussenKop)
element_h5_tussenkop_handler = SimpleGenerator("h5", TussenKop)
element_h6_tussenkop_handler = SimpleGenerator("h6", TussenKop)
a_handler = RefGenerator()


I.element_generators = [
    element_b_handler,
    element_u_handler,
    element_sub_handler,
    element_sup_handler,
    element_strong_handler,
    element_br_handler,
    a_handler,
]
B.element_generators = [
    element_i_handler,
    element_em_handler,
    element_u_handler,
    element_sub_handler,
    element_sup_handler,
    element_strong_handler,
    element_br_handler,
    a_handler,
]
U.element_generators = [
    element_i_handler,
    element_em_handler,
    element_b_handler,
    element_sub_handler,
    element_sup_handler,
    element_strong_handler,
    element_br_handler,
    a_handler,
]
Sub.element_generators = []
Sup.element_generators = []
Strong.element_generators = [
    element_i_handler,
    element_em_handler,
    element_b_handler,
    element_u_handler,
    element_sub_handler,
    element_sup_handler,
    element_br_handler,
    a_handler,
]
Al.element_generators = [
    element_i_handler,
    element_em_handler,
    element_b_handler,
    element_u_handler,
    element_sub_handler,
    element_sup_handler,
    element_strong_handler,
    element_br_handler,
    a_handler,
]
Kop.element_generators = [
    element_i_handler,
    element_em_handler,
    element_b_handler,
    element_u_handler,
    element_sub_handler,
    element_sup_handler,
    element_strong_handler,
]
TussenKop.element_generators = [
    element_i_handler,
    element_em_handler,
    element_b_handler,
    element_u_handler,
    element_sub_handler,
    element_sup_handler,
    element_strong_handler,
]
Inhoud.element_generators = [
    element_p_handler,
    element_ul_handler,
    element_ol_handler,
    element_img_handler,
    element_table_handler,
    element_h3_tussenkop_handler,
    element_h4_tussenkop_handler,
    element_h5_tussenkop_handler,
    element_h6_tussenkop_handler,
]
Li.element_generators = [
    element_p_handler,
    element_ul_handler,
    element_ol_handler,
    element_img_handler,
]
Lijst.element_generators = [
    element_li_handler,
]
Lichaam.element_generators = [
    element_div_handler,
]
Entry.element_generators = [
    element_p_handler,
    element_ul_handler,
    element_ol_handler,
    element_img_handler,
    element_h1_tussenkop_handler,
    element_h2_tussenkop_handler,
    element_h3_tussenkop_handler,
    element_h4_tussenkop_handler,
    element_h5_tussenkop_handler,
    element_h6_tussenkop_handler,
]
Row.element_generators = [element_th_handler, element_td_handler]
Tbody.element_generators = [
    element_tr_handler,
]
Thead.element_generators = [
    element_tr_handler,
]
