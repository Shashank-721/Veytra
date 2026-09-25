
#FastAPI → Service → Repository → Database

from fastapi import APIRouter, Depends, HTTPException
#APIRouter lets us group related API endpoints together.
#Depends → lets FastAPI provide dependencies such as our database session.
#get_db → gives us an AsyncSession.
#IncidentRepository → handles database operations.
#Incident → validates the incoming request data with Pydantic.
#IncidentService → contains our application logic

from backend.database.connection import get_db
from backend.database.repository import IncidentRepository
from backend.models.incident import Incident, IncidentResponse
from backend.services.incident_service import IncidentService


router = APIRouter()

@router.post("/incidents") #uses our pydantic model to validate then give the endpoint a database session and start our actual application
async def create_incident(
    incident: Incident,
    db=Depends(get_db),
):
    # Create a repository using the database session
    repository = IncidentRepository(db)

    # Create the service using the repository
    service = IncidentService(repository)

    # Create the incident through the service layer
    created_incident = await service.create_incident(incident)

    # Return the created incident
    return created_incident


@router.get("/incidents/{incident_id}",
    response_model=IncidentResponse,
)
async def get_incident(
    incident_id: str,
    db=Depends(get_db),
):
    # Create a repository using the database session
    repository = IncidentRepository(db)

    # Get the incident from the repository
    incident = await repository.get_incident(incident_id)

    #if the incident does not exist, return HTTP 404
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    # Return the incident
    return incident