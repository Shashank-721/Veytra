from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command
from backend.agents.postmortem import generate_postmortem


from backend.agents.execution import execute_remediation
from backend.agents.remediation import plan_remediation
from backend.agents.state import InvestigationState
from backend.agents.nodes import (
    start_investigation,
    collect_metrics,
    collect_logs,
    collect_deployments,
    collect_database_health,
    generate_hypotheses,
    evaluate_hypotheses,
    make_decision,
)
from backend.agents.verify import verify_remediation
from backend.agents.recovery import recover_from_failure
from backend.guardrails.check import check_remediation_risk
from backend.guardrails.approval import process_human_approval


# Create the graph using our shared investigation state.
builder = StateGraph(InvestigationState)


# Add investigation nodes.
builder.add_node("start_investigation", start_investigation)
builder.add_node("collect_metrics", collect_metrics)
builder.add_node("collect_logs", collect_logs)
builder.add_node("collect_deployments", collect_deployments)
builder.add_node("collect_database_health", collect_database_health)
builder.add_node("generate_hypotheses", generate_hypotheses)
builder.add_node("evaluate_hypotheses", evaluate_hypotheses)
builder.add_node("make_decision", make_decision)

# Add remediation nodes.
builder.add_node("plan_remediation", plan_remediation)
builder.add_node("check_remediation_risk", check_remediation_risk)
builder.add_node("process_human_approval", process_human_approval)
builder.add_node("execute_remediation", execute_remediation)

# Add verification and recovery nodes.
builder.add_node("verify_remediation", verify_remediation)
builder.add_node("recover_from_failure", recover_from_failure)
builder.add_node("generate_postmortem", generate_postmortem)


# Investigation flow.
builder.add_edge(START, "start_investigation")
builder.add_edge("start_investigation", "collect_metrics")
builder.add_edge("collect_metrics", "collect_logs")
builder.add_edge("collect_logs", "collect_deployments")
builder.add_edge("collect_deployments", "collect_database_health")
builder.add_edge("collect_database_health", "generate_hypotheses")
builder.add_edge("generate_hypotheses", "evaluate_hypotheses")
builder.add_edge("evaluate_hypotheses", "make_decision")


# Remediation flow.
builder.add_edge("make_decision", "plan_remediation")
builder.add_edge("plan_remediation", "check_remediation_risk")
builder.add_edge("check_remediation_risk", "process_human_approval")


# Decide whether the human approved the remediation.
def route_after_approval(state: InvestigationState):
    if state["approval"] == "APPROVED":
        return "execute_remediation"

    return END


builder.add_conditional_edges(
    "process_human_approval",
    route_after_approval,
)


# Verify the remediation after execution.
builder.add_edge("execute_remediation", "verify_remediation")


# Decide what to do after verification.
def route_after_verification(state: InvestigationState):
    if state["status"] == "FAILED":
        return "recover_from_failure"

    return "generate_postmortem"


builder.add_conditional_edges(
    "verify_remediation",
    route_after_verification,
)


# End after recovery.
builder.add_edge("recover_from_failure", "generate_postmortem")
builder.add_edge("generate_postmortem", END)


# Save paused workflow state.
memory = MemorySaver()

# Compile the graph.
graph = builder.compile(checkpointer=memory)


if __name__ == "__main__":
    initial_state = {
        "incident_id": "INC-001",
        "service": "checkout-api",
        "severity": "HIGH",
        "status": "OPEN",
        "evidence": [],
        "hypotheses": [],
        "evaluation": [],
        "decision": "",
        "remediation": {},
        "approval": "PENDING",
    }

    config = {
        "configurable": {
            "thread_id": "INC-001"
        }
    }

    # Run until human approval is required.
    result = graph.invoke(initial_state, config)
    print("PAUSED:", result)

    # Resume after human approval.
    result = graph.invoke(
        Command(resume="APPROVED"),
        config,
    )
    print("RESUMED:", result)