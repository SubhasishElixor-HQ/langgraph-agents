# 🤖 LangGraph Agents

### Agentic AI Workflows with LangGraph

**Reason → Act → Observe → Decide → Execute**

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square\&logo=python)](https://python.org)
[![LangGraph](https://img.shields.io/badge/LangGraph-Agentic_AI-1C3C3C?style=flat-square)]
[![LangChain](https://img.shields.io/badge/LangChain-Framework-1C3C3C?style=flat-square)]

---

## 🧠 Agentic AI

Agentic AI combines **reasoning, tools, memory, decisions, and actions** to complete multi-step tasks.

```mermaid
flowchart LR
    A([USER GOAL])
    --> B[AGENT<br/>Reason + Plan]

    B --> C{DECISION}

    C -->|Tool Needed| D[TOOL / API]
    D --> E[OBSERVE<br/>Result]

    E --> B

    C -->|Complete| F([OUTCOME])
```

**Concepts:** `Goal → Reasoning → Decision → Tool → Observation → Loop → Outcome`

---

## ⚡ LangGraph Core

LangGraph models an agent as a **stateful graph**.

```mermaid
flowchart TD
    A([START])
    --> B[STATE]

    B --> C[NODE<br/>Agent]

    C --> D{EDGE<br/>Decision}

    D -->|Tool| E[TOOL NODE]
    E --> F[UPDATE STATE]
    F --> C

    D -->|Finish| G([END])
```

### Core Concepts

```text
STATE
  │
  │ stores context
  ▼
NODES
  │
  │ execute logic
  ▼
EDGES
  │
  │ control routing
  ▼
TOOLS
  │
  │ perform actions
  ▼
OBSERVATION
  │
  │ update state
  ▼
OUTCOME
```

**State → Nodes → Edges → Tools → Observation → Outcome**

---

## 🛠️ Tool Calling

Agents can dynamically select tools based on the current state.

```mermaid
flowchart TD
    A[AGENT]
    --> B{TOOL ROUTER}

    B --> C[Web Search]
    B --> D[Python]
    B --> E[Database]
    B --> F[External API]

    C --> G[RESULT]
    D --> G
    E --> G
    F --> G

    G --> H[UPDATE STATE]
    H --> A
```

**Concepts:** `Tool Calling • Routing • State Update • Feedback Loop`

---

## 🔀 Conditional Routing

LangGraph can route execution based on decisions.

```mermaid
flowchart TD
    A[AGENT]
    --> B{CONDITIONAL EDGE}

    B -->|Research| C[Research Node]
    B -->|Code| D[Coding Node]
    B -->|Analyze| E[Analysis Node]

    C --> F[RESULT]
    D --> F
    E --> F

    F --> G{Continue?}

    G -->|Yes| A
    G -->|No| H([END])
```

**Concept:** `Node → Conditional Edge → Node`

---

## 🤝 Multi-Agent

Multiple specialized agents can work together inside one graph.

```mermaid
flowchart TD
    A([USER GOAL])
    --> B[PLANNER AGENT]

    B --> C[RESEARCH AGENT]
    B --> D[CODING AGENT]
    B --> E[ANALYSIS AGENT]

    C --> F[REVIEWER]
    D --> F
    E --> F

    F --> G([FINAL OUTCOME])
```

**Concepts:** `Planner • Specialized Agents • Coordination • Review`

---

## 🧠 State

State is the shared information flowing through the graph.

```mermaid
flowchart LR
    A[USER INPUT]
    --> B[(STATE)]

    B --> C[AGENT]
    C --> D[(UPDATED STATE)]

    D --> E[TOOL]
    E --> F[(NEW STATE)]

    F --> C
```

```text
STATE = Context + Messages + Results + Decisions
```

---

## 👤 Human-in-the-Loop

Sensitive actions can pause the graph for approval.

```mermaid
flowchart TD
    A[AGENT]
    --> B{ACTION}

    B --> C[SAFE ACTION]
    B --> D[SENSITIVE ACTION]

    D --> E[HUMAN APPROVAL]

    E -->|Approved| F[EXECUTE]
    E -->|Rejected| G[STOP / REPLAN]

    C --> H([OUTCOME])
    F --> H
```

**Concept:** `Agent → Approval → Execute → Verify → Outcome`

---

## 🏗️ Complete Workflow

```mermaid
flowchart LR
    A([GOAL])
    --> B[CONTEXT]

    B --> C[STATE]

    C --> D[AGENT]
    D --> E{DECISION}

    E -->|Tool| F[EXECUTE]
    F --> G[OBSERVE]
    G --> C

    E -->|Approval| H[HUMAN]
    H --> F

    E -->|Done| I[VERIFY]

    I --> J([OUTCOME])
```

### The Agentic Loop

**Goal → Context → State → Reason → Decide → Act → Observe → Verify → Outcome**

---


---

## ⚙️ Setup

```bash
git clone https://github.com/YOUR_USERNAME/langgraph-agents.git

cd langgraph-agents

uv venv

uv pip install -r requirements.txt

python main.py
```

Create `.env`:

```env
OPENAI_API_KEY=your_api_key
```

---

## 🎯 Learning Flow

```text
LLM
 ↓
Prompting
 ↓
Tool Calling
 ↓
Agent
 ↓
State
 ↓
LangGraph
 ↓
Conditional Routing
 ↓
Memory
 ↓
Human-in-the-Loop
 ↓
Multi-Agent
 ↓
Production Workflow
```

---

## 🚀 Vision

```text
UNDERSTAND
     ↓
REASON
     ↓
PLAN
     ↓
ACT
     ↓
OBSERVE
     ↓
VERIFY
     ↓
OUTCOME
```

### 🤖 LangGraph × Agentic AI

**Build systems that don't just answer — they execute workflows.**
