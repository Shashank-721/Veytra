from langgraph.graph import StateGraph, START, END

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


# Create a graph builder using our shared investigation state.
builder = StateGraph(InvestigationState)


# Add the first investigation node to the graph.
builder.add_node("start_investigation", start_investigation)

# Add the metrics collection node to the workflow.
builder.add_node("collect_metrics", collect_metrics)

# Add the logs collection node to the workflow.
builder.add_node("collect_logs", collect_logs)

# Add the deployment collection node to the workflow.
builder.add_node("collect_deployments", collect_deployments)

# Add the database health collection node.
builder.add_node("collect_database_health", collect_database_health)

# Add the hypothesis generation node.
builder.add_node("generate_hypotheses", generate_hypotheses)

# Evaluate the generated hypotheses against the collected evidence.
builder.add_node("evaluate_hypotheses", evaluate_hypotheses)

# Decide what should happen after evaluating the hypotheses.
builder.add_node("make_decision", make_decision)

# Create a remediation plan after the investigation.
# This node proposes an action but does NOT execute it.
builder.add_node("plan_remediation", plan_remediation)


# Start the investigation.
builder.add_edge(START, "start_investigation")

# Collect service metrics.
builder.add_edge("start_investigation", "collect_metrics")

# Collect recent application logs.
builder.add_edge("collect_metrics", "collect_logs")

# Collect recent deployments.
builder.add_edge("collect_logs", "collect_deployments")

# Collect database health.
builder.add_edge("collect_deployments", "collect_database_health")

# Generate hypotheses from the collected evidence.
builder.add_edge("collect_database_health", "generate_hypotheses")

# After generating hypotheses, evaluate them against the evidence.
builder.add_edge("generate_hypotheses", "evaluate_hypotheses")

# After evaluating hypotheses, decide what should happen next.
builder.add_edge("evaluate_hypotheses", "make_decision")

# After making the decision, create a remediation plan.
# The remediation is NOT executed yet.
builder.add_edge("make_decision", "plan_remediation")

# End the workflow after creating the remediation plan.
builder.add_edge("plan_remediation", END)


# Compile the graph into an executable workflow.
graph = builder.compile()


# Test the graph when this file is executed directly.
if __name__ == "__main__":

    # Create an initial incident investigation state.
    initial_state = {
        "incident_id": "INC-001",
        "service": "checkout-api",
        "severity": "HIGH",
        "status": "OPEN",
        "evidence": [],
        "hypotheses": [],
        "evaluation": [],

        # This will be populated by the decision node.
        "decision": "",

        # This will be populated by the remediation planning node.
        "remediation": {},

        # Human approval starts as pending.
        "approval": "PENDING",
    }

    # Run the investigation graph.
    result = graph.invoke(initial_state)

    # Print the final state returned by the graph.
    print(result)