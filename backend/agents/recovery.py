#it will have the recovery path

from backend.agents.state import InvestigationState


def recover_from_failure(state: InvestigationState):
    # Record that the previous remediation did not resolve the incident.
    state["status"] = "FAILED"

    # Mark the investigation for another attempt.
    state["decision"] = "RETRY_REMEDIATION"

    return state