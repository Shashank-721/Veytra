from backend.agents.state import InvestigationState
from backend.tools.database_provider import SIMULATED_DATABASE_HEALTH


def execute_remediation(state: InvestigationState):
    # Get the approved remediation plan.
    remediation = state["remediation"]

    # Get the action we are supposed to execute.
    action = remediation["action"]

    # Execute the supported remediation.
    if action == "increase_database_connection_pool":
        print("Executing remediation: increase database connection pool")

        # Simulate the database recovering after the remediation.
        database = SIMULATED_DATABASE_HEALTH[state["service"]]
        database["connection_pool_usage"] = 0.50
        database["active_connections"] = 50
        database["latency_ms"] = 100
        database["health"] = "HEALTHY"

        state["status"] = "VERIFYING"

    return state