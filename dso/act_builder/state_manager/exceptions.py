from typing import Any, List, Optional


class StateException(Exception):
    """Base class for all state related exceptions."""


class OWStateError(StateException):
    """OW State inconsistency related problem."""


class OWStateMutationError(OWStateError):
    """Exception raised when an attempt is made to add OW object to the state with an ID already existing."""

    def __init__(self, message: str, action: str, ow_object: dict, *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.action = action
        self.ow_object = ow_object


class OWObjectStateException(OWStateError):
    """Indicates OW State inconsistency when an object is missing expected references or is dangling."""

    def __init__(
        self, message: str, ow_object: Optional[dict] = None, ref_ow_id: Optional[str] = None, *args, **kwargs
    ):
        super().__init__(message, *args, **kwargs)
        self.ow_object = ow_object
        self.ref_ow_id = ref_ow_id


class OWStateDanglingObjectsException(OWStateError):
    """Indicates OW State inconsistency of ending up with dangling objects"""

    def __init__(self, message: str, ow_objects: List[Any], *args, **kwargs):
        super().__init__(message, *args, **kwargs)
        self.ow_objects = ow_objects
