from enum import Enum

from dso.services.koop.waardelijsten.gen import (
    StappenUitDeBesluitvormingsprocedureVoorEenDefinitiefBesluit,
    StappenUitDeBesluitvormingsprocedureVoorEenOntwerpbesluit,
)
from dso.services.utils.enum import merge_enums

ProcedureStappen: type[Enum] = merge_enums(
    "ProcedureStappen",
    StappenUitDeBesluitvormingsprocedureVoorEenDefinitiefBesluit,
    StappenUitDeBesluitvormingsprocedureVoorEenOntwerpbesluit,
)
