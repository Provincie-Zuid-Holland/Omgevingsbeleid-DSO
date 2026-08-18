from pydantic import BaseModel


class PolicyObjectReference(BaseModel):
    """
    Map object code to a generated wid for annotation and
    logging.
    """

    object_code: str
    wid: str
    location: str | None = None
    ow_location_id: str | None = None
