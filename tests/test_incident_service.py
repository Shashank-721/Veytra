import pytest
from datetime import datetime
from uuid import uuid4

from backend.database.connection import AsyncSessionLocal, init_db
from backend.database.repository import IncidentRepository
from backend.models.incident import Incident
from backend.services.incident_service import IncidentService


@pytest.mark.asyncio
async def test_create_incident_service():

    # Make sure the database and its tables exist
    await init_db()

    # Create an asynchronous database session
    async with AsyncSessionLocal() as session:

        # Create the repository using our database session
        repository = IncidentRepository(session)

        # Create the service using our repository
        service = IncidentService(repository)

        # Create a Pydantic Incident object
        incident = Incident(
            id=uuid4(),
            title="Checkout API Failure",
            description="Checkout API is returning HTTP 500 errors.",
            service="checkout-api",
            severity="HIGH",
            status="OPEN",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # Ask the service to create the incident
        created_incident = await service.create_incident(incident)

        # Verify that the incident was successfully created
        assert created_incident.id == str(incident.id)

        # Verify that the service converted the fields correctly
        assert created_incident.title == incident.title
        assert created_incident.service == incident.service
        assert created_incident.severity == incident.severity
        assert created_incident.status == incident.status