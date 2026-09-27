[README.md](https://github.com/user-attachments/files/32712370/README.md)
# Veytra

**Veytra** is an AI-powered production incident investigation and
response agent.

The goal of Veytra is to simulate how an AI agent could help investigate
production incidents by collecting operational evidence, generating and
evaluating hypotheses, deciding whether remediation is required,
applying safety guardrails, requesting human approval, executing a
remediation, verifying the result, and producing a postmortem.

Veytra is being built as a learning-focused but production-inspired
project around **GenAI, agentic workflows, tool use, and operational
automation**.

> **Project status:** Veytra is actively under development. The core
> investigation and remediation workflow is working. **MCP integration
> is currently in progress and is not finished yet.**

------------------------------------------------------------------------

## What Veytra Does

A typical Veytra investigation currently follows this flow:

``` text
Incident
   ↓
Start Investigation
   ↓
Collect Metrics
   ↓
Collect Logs
   ↓
Collect Deployments
   ↓
Collect Database Health
   ↓
Generate Hypotheses
   ↓
Evaluate Hypotheses
   ↓
Make Decision
   ↓
Plan Remediation
   ↓
Check Risk / Guardrails
   ↓
Human Approval
   ↓
Execute Remediation
   ↓
Verify Remediation
   ↓
Recover if Verification Fails
   ↓
Generate Postmortem
```

The production environment is currently **simulated**, so Veytra can be
developed and tested without connecting to real production
infrastructure.

------------------------------------------------------------------------

## Architecture

``` text
                    ┌─────────────────────┐
                    │    Streamlit UI     │
                    │    Frontend         │
                    └──────────┬──────────┘
                               │ HTTP
                               ▼
                    ┌─────────────────────┐
                    │      FastAPI        │
                    │       API           │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │     LangGraph       │
                    │ Investigation Flow  │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
        ┌───────────┐   ┌─────────────┐   ┌─────────────┐
        │ LLM       │   │ Tools       │   │ Guardrails  │
        │ Llama 3.1 │   │ Metrics     │   │ Risk checks │
        │ via HF    │   │ Logs        │   │ Approval    │
        └───────────┘   │ Deployments │   └─────────────┘
                        │ Database    │
                        └──────┬──────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Simulated Production│
                    │ Environment         │
                    └─────────────────────┘

                    MCP integration
                    ────────────────
                    Currently in progress.
                    FastMCP server/tool work has
                    started, but the MCP client
                    integration is not complete yet.
```

### Main components

  -----------------------------------------------------------------------
  Component                           Purpose
  ----------------------------------- -----------------------------------
  **LangGraph**                       Controls the stateful investigation
                                      workflow

  **LangChain**                       Connects the application to the LLM

  **Hugging Face**                    Provides the Llama 3.1 8B Instruct
                                      model through the inference API

  **FastAPI**                         Provides the backend REST API

  **SQLAlchemy + SQLite**             Persists incident state

  **Streamlit**                       Provides the user interface

  **Tools / Providers**               Simulate operational data such as
                                      metrics, logs, deployments, and
                                      database health

  **Guardrails**                      Classify remediation risk and
                                      control approval

  **FastMCP**                         Being added as the MCP interface
                                      for tools; integration is currently
                                      unfinished
  -----------------------------------------------------------------------

------------------------------------------------------------------------

## Project Structure

``` text
Veytra/
│
├── backend/
│   ├── agents/
│   │   ├── graph.py
│   │   ├── nodes.py
│   │   ├── state.py
│   │   ├── execution.py
│   │   ├── postmortem.py
│   │   ├── recovery.py
│   │   └── verify.py
│   │
│   ├── api/
│   │   └── incident_routes.py
│   │
│   ├── database/
│   │   ├── models.py
│   │   └── repository.py
│   │
│   ├── guardrails/
│   │   ├── approval.py
│   │   └── check.py
│   │
│   ├── mcp/
│   │   └── metrics_server.py
│   │
│   ├── models/
│   │   └── incident.py
│   │
│   └── main.py
│
├── frontend/
│   └── app.py
│
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

## How to Run Veytra

### 1. Clone the repository

``` bash
git clone https://github.com/Shashank-721/Veytra.git
cd Veytra
```

### 2. Create a virtual environment

Windows:

``` powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS / Linux:

``` bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root and provide the credentials
required by the current LLM setup.

For the Hugging Face integration, configure your Hugging Face API token,
for example:

``` env
HUGGINGFACEHUB_API_TOKEN=your_token_here
```

Do **not** commit your `.env` file or API keys to GitHub.

### 5. Start the FastAPI backend

From the project root:

``` bash
python -m uvicorn backend.main:app --reload
```

The API will be available at:

``` text
http://127.0.0.1:8000
```

FastAPI's interactive API documentation is available at:

``` text
http://127.0.0.1:8000/docs
```

### 6. Start the Streamlit frontend

Open another terminal, activate the virtual environment, and run:

``` bash
streamlit run frontend/app.py
```

Then open the Streamlit URL shown in the terminal.

------------------------------------------------------------------------

## Using the Application

The current UI allows you to work with an incident and:

1.  Create an incident.
2.  Start an investigation.
3.  Review collected operational evidence.
4.  Review the investigation result and remediation state.
5.  Approve the proposed remediation when human approval is required.
6.  Observe verification and resolution.
7.  Review the generated postmortem.

The simulated environment currently provides operational information
such as:

-   Request rate
-   Error rate
-   Latency
-   Recent logs
-   Recent deployments
-   Database health
-   Connection pool usage

------------------------------------------------------------------------

## API Endpoints

The backend currently exposes endpoints for the incident lifecycle,
including:

``` text
POST /incidents
GET  /incidents/{incident_id}
POST /incidents/{incident_id}/investigate
POST /incidents/{incident_id}/approve
```

The exact request and response schemas can be explored through the
FastAPI documentation at:

``` text
http://127.0.0.1:8000/docs
```

------------------------------------------------------------------------

## Example Investigation

Veytra includes a simulated `checkout-api` incident scenario.

The simulated environment can produce abnormal conditions such as:

``` text
Error rate:          7%
Latency:             850 ms
Database connections: 95 / 100
Database latency:    1200 ms
```

The agent uses the available evidence to form and evaluate hypotheses
before deciding whether remediation is required.

A remediation can then pass through:

``` text
Risk Check
    ↓
Human Approval
    ↓
Execution
    ↓
Verification
```

If verification fails, Veytra has a recovery path before generating the
final postmortem.

------------------------------------------------------------------------

## LLM

Veytra currently uses:

**Meta Llama 3.1 8B Instruct**

through the **Hugging Face Inference API**, integrated with LangChain.

The LLM is used for parts of the investigation such as:

-   Generating hypotheses
-   Evaluating hypotheses against collected evidence
-   Supporting the investigation decision

Deterministic application logic is still used for important workflow and
safety decisions rather than allowing the LLM to control everything.

------------------------------------------------------------------------

## Guardrails and Human Approval

Veytra separates investigation from remediation.

Remediation actions are classified using risk levels:

``` text
READ_ONLY
REVERSIBLE
DESTRUCTIVE
```

Actions that require approval pause the workflow and wait for a human
decision.

This is an intentional design choice:

``` text
AI investigates
      ↓
AI proposes action
      ↓
Guardrails check risk
      ↓
Human approves
      ↓
System executes
      ↓
System verifies
```

The goal is to demonstrate controlled agentic automation rather than
unrestricted autonomous production changes.

------------------------------------------------------------------------

## MCP Status

### Current status: 🚧 In Progress

MCP integration has started using **FastMCP**.

The current MCP work includes:

-   A FastMCP metrics server
-   A `get_metrics` MCP tool
-   Registration and direct execution testing of the tool
-   Starting the MCP server with stdio transport

The remaining work is to properly connect Veytra's agent/tool workflow
to the MCP server through an MCP client.

The intended architecture is:

``` text
LangGraph Agent
       ↓
    MCP Client
       ↓
 MCP Server(s)
       ↓
Operational Tools
       ↓
Metrics / Logs / Database / etc.
```

MCP is therefore **not considered complete yet** and is the next major
development area.

------------------------------------------------------------------------

## Development Roadmap

The project is being developed incrementally.

### Completed / Working

-   [x] Project architecture
-   [x] FastAPI backend
-   [x] SQLite persistence
-   [x] Incident lifecycle
-   [x] Simulated production environment
-   [x] Metrics, logs, deployments, and database tools
-   [x] LangChain + Hugging Face LLM integration
-   [x] LangGraph investigation workflow
-   [x] Evidence collection
-   [x] Hypothesis generation and evaluation
-   [x] Remediation planning
-   [x] Risk guardrails
-   [x] Human approval
-   [x] Remediation execution
-   [x] Verification
-   [x] Failure recovery
-   [x] Postmortem generation
-   [x] Streamlit frontend
-   [x] Initial MCP server/tool work

### In Progress / Planned

-   [ ] Complete MCP client integration
-   [ ] Connect LangGraph tools through MCP
-   [ ] Expand MCP servers for logs, deployments, and database
    operations
-   [ ] Improve testing and evaluation
-   [ ] LangSmith tracing/evaluation
-   [ ] Dockerization
-   [ ] AWS deployment
-   [ ] Optional RAG over runbooks and historical incidents

------------------------------------------------------------------------

## Why Veytra?

Veytra is designed to explore a practical question:

> **How can an AI agent investigate production incidents and take
> controlled remediation actions while keeping humans in the loop?**

Rather than building a generic chatbot, the project focuses on:

-   Stateful agent workflows
-   Tool use
-   Evidence-driven reasoning
-   Operational data
-   Guardrails
-   Human-in-the-loop approval
-   Verification and recovery
-   Production-inspired architecture

The project is intentionally being built step by step so that each part
of the system can be understood, tested, and replaced with real
infrastructure later.

------------------------------------------------------------------------

## Project Status

**Veytra is an active work in progress.**

The core incident investigation and controlled remediation workflow is
currently implemented. MCP integration has started but is **not complete
yet**.

More components will be added as the project evolves.
