import asyncio
from datetime import datetime
from uuid import uuid4

import pytest

from backend.database.connection import AsyncSessionLocal, init_db
from backend.database.models import IncidentDB
from backend.database.repository import IncidentRepository


@pytest.mark.asyncio
async def test_create_and_get_incident():
    # Make sure the database tables exist
    await init_db()

    # Create a database session
    async with AsyncSessionLocal() as session:

        # Create our repository
        repository = IncidentRepository(session)

        # Generate a unique ID for the incident
        incident_id = str(uuid4())

        # Create an IncidentDB object
        incident = IncidentDB(
            id=incident_id,
            title="Checkout API Failure",
            description="Checkout API is returning HTTP 500 errors.",
            service="checkout-api",
            severity="HIGH",
            status="OPEN",
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        # Save the incident to the database
        created_incident = await repository.create_incident(incident)

        # Verify that the incident was created
        assert created_incident.id == incident_id

        # Retrieve the incident from the database
        retrieved_incident = await repository.get_incident(incident_id)

        # Verify that the incident exists
        assert retrieved_incident is not None

        # Verify important fields
        assert retrieved_incident.title == "Checkout API Failure"
        assert retrieved_incident.service == "checkout-api"
        assert retrieved_incident.severity == "HIGH"
        assert retrieved_incident.status == "OPEN"


# Allows us to run this file directly with Python as well
if __name__ == "__main__":
    asyncio.run(test_create_and_get_incident())