from dso.act_builder.state_manager.input_data.besluit import Besluit, Artikel
from dso.services.koop.waardelijsten.gen import ProcedureType, RechtsgebiedType, OnderwerpType
from tests.factory import Factory


class BesluitFactory(Factory):
    def create(self) -> Besluit:
        return Besluit(
            officiele_titel="Omgevingsvisie van Zuid-Holland",
            citeertitel="",
            aanhef="<p>Vaststellingsbesluit Omgevingsvisie Provincie Zuid-Holland.</p>",
            wijzig_artikel=Artikel(
                label="Artikel",
                nummer="I",
                inhoud='De Omgevingsvisie wordt vastgesteld zoals gegeven in <IntRef ref="cmp_1">Bijlage 1</IntRef> van dit Besluit.',
            ),
            tekst_artikelen=[
                Artikel(label="Artikel", nummer="III", inhoud="<p>Hierbij nog meer tekst</p>"),
            ],
            tijd_artikel=Artikel(
                label="Artikel", nummer="II", inhoud="<Al>Deze Omgevingsvisie treedt in werking op 10 juli 2024.</Al>"
            ),
            sluiting="<p>Aldus vastgesteld in de vergadering van 3 juli 2024.</p>",
            ondertekening="<p>Gedeputeerde Staten</p>",
            rechtsgebieden=[
                RechtsgebiedType.omgevingsrecht,
            ],
            onderwerpen=[
                OnderwerpType.ruimtelijke_ordening,
            ],
            soort_procedure=ProcedureType.definitief_besluit,
            bijlagen=[],
            motivering=None,
        )
