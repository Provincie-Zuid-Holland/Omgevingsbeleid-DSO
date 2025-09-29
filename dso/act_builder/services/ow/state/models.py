from abc import abstractmethod
from enum import Enum
from typing import Annotated, List, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict, Field


class AbstractRef(BaseModel):
    @abstractmethod
    def get_key(self) -> str:
        pass

    def get_href(self) -> str:
        raise RuntimeError("Can not get href of unresolved reference")


# Locatie
class AbstractLocationRef(AbstractRef):
    ref_type: str = Field(..., description="Type discriminator")


# Ambtsgebied
class UnresolvedAmbtsgebiedRef(AbstractLocationRef):
    ref_type: Literal["unresolved_ambtsgebied"] = "unresolved_ambtsgebied"

    def get_key(self) -> str:
        return "ambtsgebied"


class AmbtsgebiedRef(UnresolvedAmbtsgebiedRef):
    ref_type: Literal["ambtsgebied"] = "ambtsgebied"
    ref: str

    def get_href(self) -> str:
        return self.ref


# Gebied
class UnresolvedGebiedRef(AbstractLocationRef):
    ref_type: Literal["unresolved_gebied"] = "unresolved_gebied"
    target_code: str

    def get_key(self) -> str:
        return self.target_code


class GebiedRef(UnresolvedGebiedRef):
    ref_type: Literal["gebied"] = "gebied"
    ref: str

    def get_href(self) -> str:
        return self.ref


# Gebiedengroep
class UnresolvedGebiedengroepRef(AbstractLocationRef):
    ref_type: Literal["unresolved_gebiedengroep"] = "unresolved_gebiedengroep"
    target_code: str

    def get_key(self) -> str:
        return self.target_code


class GebiedengroepRef(UnresolvedGebiedengroepRef):
    ref_type: Literal["gebiedengroep"] = "gebiedengroep"
    ref: str

    def get_href(self) -> str:
        return self.ref


# Define the union type for all location references
LocationRefUnion = Annotated[
    Union[
        AmbtsgebiedRef,
        UnresolvedAmbtsgebiedRef,
        GebiedRef,
        UnresolvedGebiedRef,
        GebiedengroepRef,
        UnresolvedGebiedengroepRef,
    ],
    Field(discriminator="ref_type"),
]


# Tekst / wid
class AbstractWidRef(AbstractRef):
    ref_type: str = Field(..., description="Type discriminator")

    @abstractmethod
    def get_xml_element_name(self) -> str:
        pass


#  Divisie
class UnresolvedDivisieRef(AbstractWidRef):
    ref_type: Literal["unresolved_divisie"] = "unresolved_divisie"
    target_wid: str

    def get_key(self) -> str:
        return self.target_wid

    def get_xml_element_name(self) -> str:
        return "DivisieRef"


class DivisieRef(UnresolvedDivisieRef):
    ref_type: Literal["divisie"] = "divisie"
    ref: str

    def get_href(self) -> str:
        return self.ref


# Divisietekst
class UnresolvedDivisietekstRef(AbstractWidRef):
    ref_type: Literal["unresolved_divisietekst"] = "unresolved_divisietekst"
    target_wid: str

    def get_key(self) -> str:
        return self.target_wid

    def get_xml_element_name(self) -> str:
        return "DivisietekstRef"


class DivisietekstRef(UnresolvedDivisietekstRef):
    ref_type: Literal["divisietekst"] = "divisietekst"
    ref: str

    def get_href(self) -> str:
        return self.ref


WidRefUnion = Annotated[
    Union[
        DivisieRef,
        UnresolvedDivisieRef,
        DivisietekstRef,
        UnresolvedDivisietekstRef,
    ],
    Field(discriminator="ref_type"),
]


# Objects


class OwObjectStatus(str, Enum):
    new = "new"
    changed = "changed"
    unchanged = "unchanged"
    deleted = "deleted"


class BaseOwObject(BaseModel):
    identification: str
    object_status: OwObjectStatus = Field(OwObjectStatus.unchanged)
    procedure_status: Optional[str] = Field(None)  # @deprecated?

    def assert_same_class(self, other: "BaseOwObject"):
        if type(self) is not type(other):
            raise RuntimeError("Can not handle different classes")

    def get_deleted_status(self) -> str:
        return "beëindigen"

    def is_deleted(self) -> bool:
        return self.object_status == OwObjectStatus.deleted

    def is_unchanged(self) -> bool:
        return self.object_status == OwObjectStatus.unchanged

    def flag_new(self):
        self.object_status = OwObjectStatus.new

    def flag_deleted(self):
        self.object_status = OwObjectStatus.deleted

    def flag_unchanged(self):
        self.object_status = OwObjectStatus.unchanged

    def flag_changed(self):
        self.object_status = OwObjectStatus.changed

    @abstractmethod
    def get_key(self) -> str:
        pass

    @abstractmethod
    def is_key_equal(self, other: "BaseOwObject") -> bool:
        pass

    @abstractmethod
    def is_data_equal(self, other: "BaseOwObject") -> bool:
        pass

    @abstractmethod
    def merge_from(self, other: "BaseOwObject") -> bool:
        pass

    model_config = ConfigDict(arbitrary_types_allowed=True)


class OwAmbtsgebied(BaseOwObject):
    source_uuid: str
    administrative_borders_id: str
    domain: str
    valid_on: str
    title: str

    def get_key(self) -> str:
        return "ambtsgebied"

    def is_key_equal(self, other: "OwAmbtsgebied") -> bool:
        self.assert_same_class(other)
        # Ambtsgebied is a bit special as there can only be one
        return True

    def __hash__(self):
        return hash(("ambtsgebied",))

    def __eq__(self, other: "OwAmbtsgebied"):
        return self.is_key_equal(other)

    def is_data_equal(self, other: "OwAmbtsgebied") -> bool:
        self.assert_same_class(other)
        # fmt: off
        return (
            (self.administrative_borders_id, self.domain, self.valid_on, self.title)
            ==
            (other.administrative_borders_id, other.domain, other.valid_on, other.title)
        )
        # fmt: on

    def merge_from(self, other: "OwAmbtsgebied") -> bool:
        if self.is_data_equal(other):
            self.flag_unchanged()
            return
        self.procedure_status = other.procedure_status
        self.source_uuid = other.source_uuid
        self.administrative_borders_id = other.administrative_borders_id
        self.domain = other.domain
        self.valid_on = other.valid_on
        self.title = other.title
        self.flag_changed()


class OwRegelingsgebied(BaseOwObject):
    source_uuid: str
    locatie_ref: LocationRefUnion

    def get_key(self) -> str:
        return "regelingsgebied"

    def is_key_equal(self, other: "OwRegelingsgebied") -> bool:
        self.assert_same_class(other)
        # There can only be one
        return True

    def __hash__(self):
        return hash(("regelingsgebied",))

    def __eq__(self, other: "OwRegelingsgebied"):
        return self.is_key_equal(other)

    def is_data_equal(self, other: "OwRegelingsgebied") -> bool:
        self.assert_same_class(other)
        return self.source_uuid == other.source_uuid

    def merge_from(self, other: "OwRegelingsgebied") -> bool:
        if self.is_data_equal(other):
            self.flag_unchanged()
            return
        self.procedure_status = other.procedure_status
        self.source_uuid = other.source_uuid
        self.locatie_ref = other.locatie_ref
        self.flag_changed()


class OwGebied(BaseOwObject):
    source_uuid: str
    source_code: str
    title: str
    geometry_ref: str

    def get_key(self) -> str:
        return self.source_code

    def is_key_equal(self, other: "OwGebied") -> bool:
        self.assert_same_class(other)
        return self.get_key() == other.get_key()

    def __hash__(self):
        return hash((self.source_code,))

    def __eq__(self, other: "OwGebied"):
        return self.is_key_equal(other)

    def is_data_equal(self, other: "OwGebied") -> bool:
        self.assert_same_class(other)
        return (self.title, self.geometry_ref) == (other.title, other.geometry_ref)

    def merge_from(self, other: "OwGebied") -> bool:
        self.source_uuid = other.source_uuid
        self.source_code = other.source_code
        if self.is_data_equal(other):
            self.flag_unchanged()
            return
        self.procedure_status = other.procedure_status
        self.title = other.title
        self.geometry_ref = other.geometry_ref
        self.flag_changed()


class OwGebiedengroep(BaseOwObject):
    source_uuid: str
    source_code: str
    title: str
    gebieden_refs: List[LocationRefUnion] = Field(default_factory=list)

    def get_key(self) -> str:
        return self.source_code

    def is_key_equal(self, other: "OwGebiedengroep") -> bool:
        self.assert_same_class(other)
        return self.get_key() == other.get_key()

    def __hash__(self):
        return hash((self.source_code,))

    def __eq__(self, other: "OwGebiedengroep"):
        return self.is_key_equal(other)

    def is_data_equal(self, other: "OwGebiedengroep") -> bool:
        self.assert_same_class(other)
        # fmt: off
        return (
            (self.title, [r.get_key() for r in self.gebieden_refs])
            ==
            (other.title, [r.get_key() for r in other.gebieden_refs])
        )
        # fmt: on

    def merge_from(self, other: "OwGebiedengroep") -> bool:
        self.source_uuid = other.source_uuid
        self.source_code = other.source_code
        if self.is_data_equal(other):
            self.flag_unchanged()
            return
        self.procedure_status = other.procedure_status
        self.title = other.title
        self.gebieden_refs = other.gebieden_refs
        self.flag_changed()


class OwDivisie(BaseOwObject):
    source_uuid: str
    source_code: str
    wid: str

    def get_key(self) -> str:
        return self.wid

    def is_key_equal(self, other: "OwDivisie") -> bool:
        self.assert_same_class(other)
        return self.get_key() == other.get_key()

    def __hash__(self):
        return hash((self.wid,))

    def __eq__(self, other: "OwDivisie"):
        return self.is_key_equal(other)

    def is_data_equal(self, other: "OwDivisie") -> bool:
        self.assert_same_class(other)
        return self.wid == other.wid

    def merge_from(self, other: "OwDivisie") -> bool:
        self.source_uuid = other.source_uuid
        self.source_code = other.source_code
        if self.is_data_equal(other):
            self.flag_unchanged()
            return
        self.procedure_status = other.procedure_status
        self.wid = other.wid
        self.flag_changed()


class OwDivisietekst(BaseOwObject):
    source_uuid: str
    source_code: str
    wid: str

    def get_key(self) -> str:
        return self.wid

    def is_key_equal(self, other: "OwDivisietekst") -> bool:
        self.assert_same_class(other)
        return self.get_key() == other.get_key()

    def __hash__(self):
        return hash((self.wid,))

    def __eq__(self, other: "OwDivisietekst"):
        return self.is_key_equal(other)

    def is_data_equal(self, other: "OwDivisietekst") -> bool:
        self.assert_same_class(other)
        return self.wid == other.wid

    def merge_from(self, other: "OwDivisietekst") -> bool:
        self.source_uuid = other.source_uuid
        self.source_code = other.source_code
        if self.is_data_equal(other):
            self.flag_unchanged()
            return
        self.procedure_status = other.procedure_status
        self.wid = other.wid
        self.flag_changed()


class OwGebiedsaanwijzing(BaseOwObject):
    source_code: str
    title: str
    indication_type: str
    indication_group: str
    location_refs: List[LocationRefUnion] = Field(default_factory=list)

    def get_key(self) -> str:
        return self.source_code

    def is_key_equal(self, other: "OwGebiedsaanwijzing") -> bool:
        self.assert_same_class(other)
        return self.get_key() == other.get_key()

    def __hash__(self):
        return hash((self.source_code,))

    def __eq__(self, other: "OwGebiedsaanwijzing"):
        return self.is_key_equal(other)

    def is_data_equal(self, other: "OwGebiedsaanwijzing") -> bool:
        self.assert_same_class(other)
        # fmt: off
        return (
            (self.title, self.indication_type, self.indication_group, [r.get_key() for r in self.location_refs])
            ==
            (other.title, self.indication_type, self.indication_group, [r.get_key() for r in other.location_refs])
        )
        # fmt: on

    def merge_from(self, other: "OwGebiedsaanwijzing") -> bool:
        self.source_code = other.source_code
        if self.is_data_equal(other):
            self.flag_unchanged()
            return
        self.procedure_status = other.procedure_status
        self.title = other.title
        self.indication_type = other.indication_type
        self.indication_group = other.indication_group
        self.location_refs = other.location_refs
        self.flag_changed()


class OwTekstdeel(BaseOwObject):
    source_uuid: str
    source_code: str
    idealization: str
    text_ref: WidRefUnion
    location_refs: List[LocationRefUnion] = Field(default_factory=list)

    def get_key(self) -> str:
        return self.source_code

    def is_key_equal(self, other: "OwTekstdeel") -> bool:
        self.assert_same_class(other)
        return self.get_key() == other.get_key()

    def __hash__(self):
        return hash((self.source_code,))

    def __eq__(self, other: "OwTekstdeel"):
        return self.is_key_equal(other)

    def is_data_equal(self, other: "OwTekstdeel") -> bool:
        self.assert_same_class(other)
        # fmt: off
        return (
            (self.idealization, self.text_ref.get_key(), [r.get_key() for r in self.location_refs])
            ==
            (other.idealization, other.text_ref.get_key(), [r.get_key() for r in other.location_refs])
        )
        # fmt: on

    def merge_from(self, other: "OwTekstdeel") -> bool:
        self.source_uuid = other.source_uuid
        self.source_code = other.source_code
        if self.is_data_equal(other):
            self.flag_unchanged()
            return
        self.procedure_status = other.procedure_status
        self.idealization = other.idealization
        self.text_ref = other.text_ref
        self.location_refs = other.location_refs
        self.flag_changed()
