from datetime import datetime
from pydantic import BaseModel
from uuid import UUID
from typing import Literal

class Incident(BaseModel):
    id : UUID
    title : str
    description : str
    service : str
    severity : Literal['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
    status : Literal['OPEN', 'INVESTIGATING', 'AWAITING_APPROVAL', 'REMEDIATING', 'VERIFYING', 'RESOLVED', 'FAILED']
    created_at : datetime
    updated_at : datetime

class IncidentResponse(BaseModel):
    id: UUID
    title: str
    description: str
    service: str
    severity: Literal["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    status: Literal[
        "OPEN",
        "INVESTIGATING",
        "AWAITING_APPROVAL",
        "REMEDIATING",
        "VERIFYING",
        "RESOLVED",
        "FAILED",
    ]
    created_at: datetime
    updated_at: datetime