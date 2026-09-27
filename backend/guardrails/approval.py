from langgraph.types import interrupt
from backend.agents.state import InvestigationState


def process_human_approval(state: InvestigationState):
    # Pause the workflow and ask for a human approval decision.
    decision = interrupt({
        "message": "Human approval required for remediation.",
        "remediation": state["remediation"],
    })

    # Store the human's decision in the investigation state.
    state["approval"] = decision

    # Move to remediation when the human approves.
    if decision == "APPROVED":
        state["status"] = "REMEDIATING"

    # Stop the workflow when the human rejects.
    elif decision == "REJECTED":
        state["status"] = "FAILED"

    return state