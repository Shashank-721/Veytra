import streamlit as st
import requests


API_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="Veytra",
    page_icon="🤖",
    layout="wide",
)


# Store the current investigation result.
if "result" not in st.session_state:
    st.session_state.result = None

if "incident_id" not in st.session_state:
    st.session_state.incident_id = ""


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def get_evidence(result, evidence_type):
    for item in result.get("evidence", []):
        if item.get("type") == evidence_type:
            return item.get("data", {})

    return None


def get_database_before(result):
    database_health = get_evidence(
        result,
        "database_health",
    )

    if database_health:
        return database_health.get("database", {})

    return None


def get_database_after(result):
    verification = get_evidence(
        result,
        "verification",
    )

    if verification:
        return verification.get("database", {})

    return None


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("Veytra")

st.subheader(
    "Autonomous Production Incident Investigation"
)

st.write(
    "Veytra investigates production incidents, "
    "identifies likely causes, proposes remediation, "
    "and requests human approval."
)

st.divider()


# ---------------------------------------------------------
# Incident investigation
# ---------------------------------------------------------

st.header("Incident Investigation")

incident_id = st.text_input(
    "Incident ID",
    value=st.session_state.incident_id,
    placeholder="Enter incident UUID",
)


if st.button("Investigate Incident"):

    if not incident_id:
        st.warning("Please enter an incident ID.")

    else:
        response = requests.post(
            f"{API_URL}/incidents/{incident_id}/investigate"
        )

        if response.status_code == 200:

            st.session_state.incident_id = incident_id
            st.session_state.result = response.json()

            st.rerun()

        else:
            st.error(
                f"Investigation failed: {response.text}"
            )


# ---------------------------------------------------------
# Display investigation result
# ---------------------------------------------------------

result = st.session_state.result

if result:

    service = result.get(
        "service",
        "Unknown",
    )

    severity = result.get(
        "severity",
        "Unknown",
    )

    status = result.get(
        "status",
        "Unknown",
    )


    # -----------------------------------------------------
    # Incident summary
    # -----------------------------------------------------

    st.divider()
    st.header("Incident Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption("Service")
        st.metric("Service", service)

    with col2:
        st.caption("Severity")
        st.metric("Severity", severity)

    with col3:
        st.caption("Status")
        st.metric("Status", status)


    # -----------------------------------------------------
    # What is the issue?
    # -----------------------------------------------------

    st.header("What is the issue?")

    root_cause = result.get(
        "root_cause",
        "No root cause identified.",
    )

    st.info(root_cause)


    # -----------------------------------------------------
    # Key evidence
    # -----------------------------------------------------

    st.header("Key Evidence")

    metrics = get_evidence(
        result,
        "metrics",
    )

    database = get_database_before(result)

    if metrics and database:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Error Rate",
                f"{metrics.get('error_rate', 0) * 100:.1f}%",
            )

        with col2:
            st.metric(
                "Service Latency",
                f"{metrics.get('latency_ms', 0)} ms",
            )

        with col3:
            st.metric(
                "Service Health",
                metrics.get(
                    "health",
                    "UNKNOWN",
                ),
            )


        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "DB Pool Usage",
                f"{database.get('connection_pool_usage', 0) * 100:.0f}%",
            )

        with col2:
            st.metric(
                "Active Connections",
                database.get(
                    "active_connections",
                    0,
                ),
            )

        with col3:
            st.metric(
                "DB Health",
                database.get(
                    "health",
                    "UNKNOWN",
                ),
            )


    # -----------------------------------------------------
    # What can Veytra change?
    # -----------------------------------------------------

    st.divider()
    st.header("What can Veytra change?")

    remediation = result.get(
        "remediation",
        {},
    )

    if remediation:

        st.write(
            f"**Action:** "
            f"{remediation.get('action', 'Unknown')}"
        )

        st.write(
            f"**Target:** "
            f"{remediation.get('target', 'Unknown')}"
        )

        st.write(
            f"**Risk Level:** "
            f"{remediation.get('risk_level', 'Unknown')}"
        )

        st.write(
            f"**Reason:** "
            f"{remediation.get('reason', 'Unknown')}"
        )


    # -----------------------------------------------------
    # Human approval
    # -----------------------------------------------------

    approval = result.get(
        "approval",
    )

    current_status = result.get(
        "status",
    )

    if (
        current_status == "AWAITING_APPROVAL"
        and approval == "PENDING"
    ):

        st.warning(
            "Human approval is required before "
            "Veytra executes this change."
        )

        if st.button("Approve Remediation"):

            response = requests.post(
                f"{API_URL}/incidents/"
                f"{st.session_state.incident_id}/approve",
                params={
                    "decision": "APPROVED"
                },
            )

            if response.status_code == 200:

                st.session_state.result = response.json()

                st.success(
                    "Remediation approved and executed."
                )

                st.rerun()

            else:

                st.error(
                    f"Remediation failed: {response.text}"
                )


    # -----------------------------------------------------
    # After remediation
    # -----------------------------------------------------

    after_database = get_database_after(
        result
    )

    if after_database:

        st.divider()
        st.header("After Remediation")

        st.success(
            "Veytra executed the approved change "
            "and verified the result."
        )


        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                "DB Pool Usage",
                f"{after_database.get('connection_pool_usage', 0) * 100:.0f}%",
            )

        with col2:
            st.metric(
                "Active Connections",
                after_database.get(
                    "active_connections",
                    0,
                ),
            )

        with col3:
            st.metric(
                "DB Latency",
                f"{after_database.get('latency_ms', 0)} ms",
            )

        with col4:
            st.metric(
                "DB Health",
                after_database.get(
                    "health",
                    "UNKNOWN",
                ),
            )


        # -------------------------------------------------
        # Before vs After
        # -------------------------------------------------

        st.subheader("Before vs After")

        comparison = {
            "DB Pool Usage": [
                f"{database.get('connection_pool_usage', 0) * 100:.0f}%",
                f"{after_database.get('connection_pool_usage', 0) * 100:.0f}%",
            ],

            "Active Connections": [
                database.get(
                    "active_connections",
                    0,
                ),

                after_database.get(
                    "active_connections",
                    0,
                ),
            ],

            "DB Latency": [
                f"{database.get('latency_ms', 0)} ms",
                f"{after_database.get('latency_ms', 0)} ms",
            ],

            "DB Health": [
                database.get(
                    "health",
                    "UNKNOWN",
                ),

                after_database.get(
                    "health",
                    "UNKNOWN",
                ),
            ],
        }


        # Convert all values to strings so Streamlit/PyArrow
        # sees a consistent data type in each dataframe column.

        comparison_table = {
            "Metric": list(comparison.keys()),

            "Before": [
                str(values[0])
                for values in comparison.values()
            ],

            "After": [
                str(values[1])
                for values in comparison.values()
            ],
        }

        st.table(comparison_table)


    # -----------------------------------------------------
    # Resolution
    # -----------------------------------------------------

    resolution = result.get(
        "resolution",
    )

    if resolution:

        st.divider()
        st.header("Resolution")

        if result.get("status") == "RESOLVED":

            st.success("Incident resolved.")

        else:

            st.warning(
                f"Incident status: "
                f"{result.get('status')}"
            )

        st.write(resolution)

    # -----------------------------------------------------
    # Incident Postmortem
    # -----------------------------------------------------

    postmortem = result.get(
        "postmortem",
        {},
    )

    if postmortem:

        st.divider()
        st.header("Incident Postmortem")

        st.write(
            "**Summary:**",
            postmortem.get(
                "summary",
                "No summary available.",
            ),
        )

        st.write(
            "**Root Cause:**",
            postmortem.get(
                "root_cause",
                "No root cause identified.",
            ),
        )

        st.write(
            "**Resolution:**",
            postmortem.get(
                "resolution",
                "No resolution recorded.",
            ),
        )

        st.write(
            "**Status:**",
            postmortem.get(
                "status",
                "Unknown",
            ),
        )

        st.subheader("Evidence")

        evidence = postmortem.get(
            "evidence",
            [],
        )

        for item in evidence:

            evidence_type = item.get(
                "type",
                "unknown",
            )

            data = item.get("data", {})

            # Show metrics in a human-readable format.
            if evidence_type == "metrics":

                st.write("**Service Metrics**")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Error Rate",
                        f"{data.get('error_rate', 0) * 100:.1f}%",
                    )

                with col2:
                    st.metric(
                        "Latency",
                        f"{data.get('latency_ms', 0)} ms",
                    )

                with col3:
                    st.metric(
                        "Service Health",
                        data.get("health", "Unknown"),
                    )


            # Show logs as readable messages.
            elif evidence_type == "logs":

                st.write("**Recent Logs**")

                for log in data.get("logs", []):
                    st.write(f"- {log}")


            # Show deployments as readable information.
            elif evidence_type == "deployments":

                st.write("**Recent Deployments**")

                for deployment in data.get("deployments", []):
                    st.write(
                        f"- Version **{deployment.get('version', 'Unknown')}** "
                        f"deployed at {deployment.get('deployed_at', 'Unknown')}"
                    )


            # Show database health as readable metrics.
            elif evidence_type == "database_health":

                database_data = data.get(
                    "database",
                    {},
                )

                st.write("**Database Health**")

                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric(
                        "Connection Pool Usage",
                        f"{database_data.get('connection_pool_usage', 0) * 100:.0f}%",
                    )

                with col2:
                    st.metric(
                        "Active Connections",
                        f"{database_data.get('active_connections', 0)} / "
                        f"{database_data.get('max_connections', 0)}",
                    )

                with col3:
                    st.metric(
                        "Database Health",
                        database_data.get(
                            "health",
                            "Unknown",
                        ),
                    )

                st.write(
                    f"**Database:** "
                    f"{database_data.get('database', 'Unknown')}"
                )

                st.write(
                    f"**Database Latency:** "
                    f"{database_data.get('latency_ms', 0)} ms"
                )


            # Show verification as the result after remediation.
            elif evidence_type == "verification":

                database_data = data.get(
                    "database",
                    {},
                )

                st.write("**Verification Result**")

                st.success(
                    f"Database health after remediation: "
                    f"{database_data.get('health', 'Unknown')}"
                )

                st.write(
                    f"Connection pool usage: "
                    f"{database_data.get('connection_pool_usage', 0) * 100:.0f}%"
                )

                st.write(
                    f"Database latency: "
                    f"{database_data.get('latency_ms', 0)} ms"
                )