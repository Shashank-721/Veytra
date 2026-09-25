#working as a middleman between pydantic and db
#here we get the pydantic data from the api (create,commit, post) then we get it and convert it using sqlalchemy
#and then our repository will do the post (get) commit into our db

from datetime import datetime

from backend.models.incident import Incident
from backend.database.models import IncidentDB
from backend.database.repository import IncidentRepository


class IncidentService:

    def __init__(self, repository: IncidentRepository):
        # Store the repository so the service can use database operations
        self.repository = repository

    async def create_incident(self, incident: Incident) -> IncidentDB:
        # Convert the Pydantic Incident into a SQLAlchemy IncidentDB object
        incident_db = IncidentDB(
            id=str(incident.id),
            title=incident.title,
            description=incident.description,
            service=incident.service,
            severity=incident.severity,
            status=incident.status,
            created_at=incident.created_at,
            updated_at=datetime.now(),
        )

        # Ask the repository to save the incident in the database
        created_incident = await self.repository.create_incident(incident_db)

        # Return the saved database object
        return created_incident