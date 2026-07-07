from typing import TypedDict, Optional
from app.models.reservation import Reservation


class GraphState(TypedDict):

    user_input: str
    response: str
    reservation: Optional[Reservation]
    admin_required: bool
    mcp_synced: bool