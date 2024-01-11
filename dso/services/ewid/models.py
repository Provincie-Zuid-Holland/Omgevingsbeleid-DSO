from typing import Optional

from pydantic import BaseModel


class PolicyObjectReference(BaseModel):
    """
    Map object code to a generated wid for annotation and
    logging.
    """

    object_code: str
    wid: str
    location: Optional[str] = None
    ow_location_id: Optional[str] = None
