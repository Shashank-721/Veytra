#is the layer that actually talks to the database, saving and fetching incidents.
#So, for example, it has the create incident function that saves a row, and get incident that fetches one by ID.
#So essentially, it's the part that reads from and writes to the database

# SQLAlchemy query builder
from sqlalchemy import select

# SQLAlchemy async session used for database operations
from sqlalchemy.ext.asyncio import AsyncSession

from .models import IncidentDB


# Handles database operations related to incidents
class IncidentRepository:

    # Receive a database session that this repository will use
    def __init__(self, session: AsyncSession):
        self.session = session

    # Create and save a new incident in the database
    async def create_incident(self, incident: IncidentDB) -> IncidentDB:
        self.session.add(incident)

        # Save the changes to the database
        await self.session.commit()

        # Refresh the object with the latest database state
        await self.session.refresh(incident)

        return incident

    # Get an incident by its ID
    async def get_incident(self, incident_id: str) -> IncidentDB | None:
        # Build a SELECT query for the requested incident
        query = select(IncidentDB).where(IncidentDB.id == incident_id)

        # Execute the query using our async database session
        result = await self.session.execute(query)

        # Return the incident if found, otherwise return None
        return result.scalar_one_or_none()