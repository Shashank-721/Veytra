
#FastAPI → Service → Repository → Database
from backend.agents.graph import graph
from fastapi import APIRouter, Depends, HTTPException
from langgraph.types import Command
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

@router.post("/incidents/{incident_id}/investigate")
async def investigate_incident(
    incident_id: str,
    db=Depends(get_db),
):
    # Get the incident from the database.
    repository = IncidentRepository(db)
    incident = await repository.get_incident(incident_id)

    # Return 404 if the incident does not exist.
    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    # Build the initial state for Veytra.
    initial_state = {
        "incident_id": incident.id,
        "service": incident.service,
        "severity": incident.severity,
        "status": incident.status,
        "evidence": [],
        "hypotheses": [],
        "evaluation": [],
        "decision": "",
        "remediation": {},
        "approval": "PENDING",
        "postmortem": {},
        "root_cause": "",
        "resolution": "",
    }

    # Use the incident ID as the LangGraph thread ID.
    config = {
        "configurable": {
            "thread_id": incident.id
        }
    }

    # Start the Veytra investigation.
    result = graph.invoke(
        initial_state,
        config,
    )

    await repository.update_status(
        incident_id,
        result["status"],
    )

    return result #allow you to use the original repository (db) you created to you can update it

@router.post("/incidents/{incident_id}/approve")
async def approve_incident(
    incident_id: str,
    decision: str,
    db=Depends(get_db),
):
    # Use the incident ID as the LangGraph thread ID.
    config = {
        "configurable": {
            "thread_id": incident_id
        }
    }

    # Resume the paused investigation with the human decision.
    result = graph.invoke(
        Command(resume=decision),
        config,
    )

    repository = IncidentRepository(db)

    await repository.update_status(
        incident_id,
        result["status"],
        result.get("root_cause"),
    )

    return result