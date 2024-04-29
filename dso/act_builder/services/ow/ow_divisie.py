from typing import Optional

from ....models import ContentType
from ....services.ow import (
    IMOWTYPES,
    Annotation,
    OWDivisie,
    OWDivisieTekst,
    OWObjectGenerationError,
    OwProcedureStatus,
    OWTekstDeel,
    generate_ow_id,
)
from ....services.utils.helpers import load_template
from ...state_manager import OutputFile, OWObjectStateException, OWStateRepository, StrContentData


class OwDivisieBuilder:
    def __init__(
        self,
        provincie_id: str,
        annotation_lookup_map: dict,
        ow_repository: OWStateRepository,
        ow_procedure_status: Optional[OwProcedureStatus],
    ) -> None:
        self._provincie_id = provincie_id
        self._annotation_lookup = annotation_lookup_map
        self._ow_repository = ow_repository
        self._ow_procedure_status = ow_procedure_status

    def handle_divisie_changes(self):
        annotations = []  # put in ow repo
        for object_code, values in self._annotation_lookup.items():
            existing_divisie_id = self._ow_repository.get_existing_divisie_id(values["wid"])
            if existing_divisie_id:
                previous_gebied_code = self._ow_repository.get_existing_werkingsgebied_code_by_divisie(
                    existing_divisie_id
                )
                if not previous_gebied_code:
                    continue

                if values["gebied_code"] != previous_gebied_code:
                    # owtekstdeel mutation needed since gebied annotation was changed for this wid
                    ow_tekstdeel = self._ow_repository.get_existing_tekstdeel_by_divisie(existing_divisie_id)
                    if not ow_tekstdeel:
                        raise OWObjectStateException(
                            message="Expected to find tekstdeel for existing divisie", ref_ow_id=existing_divisie_id
                        )

                    # find new / mutated OW groep created earlier to update for tekstdeel with
                    ow_gebiedengroep = self._ow_repository.get_gebiedengroep_by_code(values["gebied_code"])
                    if not ow_gebiedengroep:
                        raise OWObjectStateException(
                            message=f"Expected gebiedengroep with werkingsgebied: {values['gebied_code']} in new state",
                            ref_ow_id=values["gebied_code"],
                        )

                    ow_tekstdeel.locations = [ow_gebiedengroep.OW_ID]
                    self._ow_repository.add_mutated_ow(ow_tekstdeel)

            else:
                # Unknown wid so new division + tekstdeel annotation
                new_div = self._new_divisie(values["tag"], values["wid"])
                ow_location_id = self._ow_repository.get_active_ow_location_id(values["gebied_code"])
                new_text_mapping = self._new_text_mapping(new_div.OW_ID, ow_location_id)
                annotations.append(Annotation(divisie_aanduiding=new_div, tekstdeel=new_text_mapping))

    def _new_divisie(self, tag, wid) -> OWDivisie | OWDivisieTekst:
        if tag == "Divisietekst":
            ow_div = OWDivisieTekst(
                OW_ID=generate_ow_id(IMOWTYPES.DIVISIETEKST, self._provincie_id),
                wid=wid,
                procedure_status=self._ow_procedure_status,
            )
        elif tag == "Divisie":
            ow_div = OWDivisie(
                OW_ID=generate_ow_id(IMOWTYPES.DIVISIE, self._provincie_id),
                wid=wid,
                procedure_status=self._ow_procedure_status,
            )
        else:
            raise OWObjectGenerationError("Expected annotation text tag to be either Divisie or Divisietekst.")
        self._ow_repository.add_new_ow(ow_div)
        return ow_div

    def _new_text_mapping(self, ow_div_id, ow_location_id) -> OWTekstDeel:
        ow_text_mapping = OWTekstDeel(
            OW_ID=generate_ow_id(IMOWTYPES.TEKSTDEEL, self._provincie_id),
            divisie=ow_div_id,
            locations=[ow_location_id],
            procedure_status=self._ow_procedure_status,
        )
        self._ow_repository.add_new_ow(ow_text_mapping)
        return ow_text_mapping

    def create_file(self, output_data: dict):
        content = load_template(
            "ow/owDivisie.xml",
            pretty_print=True,
            data=output_data,
        )
        output_file = OutputFile(
            filename="owDivisie.xml",
            content_type=ContentType.XML,
            content=StrContentData(content),
        )
        return output_file
