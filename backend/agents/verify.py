from backend.agents.state import InvestigationState
from backend.tools.database import get_database_health


def verify_remediation(state: InvestigationState):
    # Check the database health after remediation.
    database_health = get_database_health(state["service"])

    # Store the verification result as new evidence.
    state["evidence"].append({
        "type": "verification",
        "data": database_health,
    })

    # Determine whether the database is healthy.
    health = database_health["database"]["health"]

    if health == "HEALTHY":
        state["status"] = "RESOLVED"
        state["resolution"] = "Database connection pool increased successfully."
    else:
        state["status"] = "FAILED"

    return state