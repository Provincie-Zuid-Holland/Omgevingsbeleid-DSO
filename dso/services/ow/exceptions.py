# General purpose exception for errors within OW object generation
class OWObjectGenerationError(Exception):
    pass


class OWTextAttributesError(Exception):
    """Exception while handling the stop xml layer of OW annotation"""
