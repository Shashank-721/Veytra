from backend.agents.state import InvestigationState


def generate_postmortem(state: InvestigationState):
    """
    Create a simple human-readable summary of the incident.
    """

    postmortem = {
        "incident_id": state["incident_id"],
        "service": state["service"],
        "severity": state["severity"],
        "status": state["status"],
        "summary": (
            f"The {state['service']} incident was investigated and "
            f"the root cause was identified as: {state['root_cause']}."
        ),
        "root_cause": state["root_cause"],
        "evidence": state["evidence"],
        "resolution": state["resolution"],
        "decision": state["decision"],
        "remediation": state["remediation"],
        "approval": state["approval"],
    }

    state["postmortem"] = postmortem

    print("POSTMORTEM:", state["postmortem"])

    return state