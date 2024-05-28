from ..ow.models import OWGebied, OWGebiedenGroep, OWAmbtsgebied, OWLocatie, OWDivisie, OWDivisieTekst, OWTekstdeel

#
# TODO: NO longer used using jinja tests
#


def is_OWAmbtsgebied(obj):
    return isinstance(obj, OWAmbtsgebied)


def is_OWLocatie(obj):
    return isinstance(obj, OWLocatie)


def is_OWDivisie(obj):
    return isinstance(obj, OWDivisie)


def is_OWDivisieTekst(obj):
    return isinstance(obj, OWDivisieTekst)


def is_OWTekstdeel(obj):
    return isinstance(obj, OWTekstdeel)


def is_OWGebied(obj):
    return isinstance(obj, OWGebied)


def is_OWGebiedenGroep(obj):
    return isinstance(obj, OWGebiedenGroep)


template_tests = {
    "OWAmbtsgebied": is_OWAmbtsgebied,
    "OWLocatie": is_OWLocatie,
    "OWGebied": is_OWGebied,
    "OWGebiedenGroep": is_OWGebiedenGroep,
    "OWDivisie": is_OWDivisie,
    "OWDivisieTekst": is_OWDivisieTekst,
    "OWTekstdeel": is_OWTekstdeel,
}
