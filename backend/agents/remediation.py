from backend.agents.state import InvestigationState
from backend.guardrails.policy import RiskLevel


def plan_remediation(state: InvestigationState):
    """
    Create a remediation plan based on the investigation result.

    The agent only plans the action here.
    It does NOT execute anything yet.
    """

    # For our simulated incident, the strongest evidence
    # points toward database connection pool exhaustion.
    action = {
        "action": "increase_database_connection_pool",
        "target": state["service"],
        "risk_level": RiskLevel.REVERSIBLE.value,
        "reason": (
            "Database connection pool usage is 95% "
            "with connection pool exhaustion errors."
        ),
        "requires_approval": True,
    }

    # Store the proposed action in the investigation state.
    state["remediation"] = action

    # Move the incident into the approval stage.
    state["status"] = "AWAITING_APPROVAL"

    return state