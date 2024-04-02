class EIDGenerationError(Exception):
    def __init__(self, element, message="Error in generating eID"):
        self.element = element
        self.message = message
        super().__init__(self.message)
