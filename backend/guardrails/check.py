from backend.agents.state import InvestigationState
from backend.guardrails.policy import RiskLevel, requires_approval


def check_remediation_risk(state: InvestigationState):
    """
    Check the risk level of the planned remediation
    and determine whether human approval is required.
    """

    remediation = state["remediation"]

    risk_level = RiskLevel(remediation["risk_level"])

    if requires_approval(risk_level):
        state["status"] = "AWAITING_APPROVAL"
    else:
        state["approval"] = "APPROVED"

    return state