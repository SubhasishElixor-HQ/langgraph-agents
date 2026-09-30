# 🤖 AI LinkedIn Post Generator

An AI-powered LinkedIn content generation system built with **Python, LangChain, LangGraph, Ollama, and Tavily**.

The project uses an **agentic workflow** where an AI Writer generates a LinkedIn post, optionally researches current information using web search, and an AI Reviewer evaluates the post. If the reviewer rejects the draft, the system sends feedback back to the Writer and generates an improved version.

---

## 🚀 Project Overview

Traditional LLM applications often follow:

```text
User → LLM → Response
```

This project uses a more structured AI workflow:

```text
User Topic
     ↓
Writer Agent
     ↓
Web Research (if required)
     ↓
Draft LinkedIn Post
     ↓
Reviewer Agent
     ↓
Approved?
   ↙     ↘
 YES      NO
  ↓        ↓
Final    Feedback
Post       ↓
        Writer Agent
           ↓
       Improved Draft
```

The workflow is implemented using **LangGraph**, allowing the system to maintain state, call tools, make decisions, and loop through revisions.

---

# 🎯 Project Objective

The goal of this project is to build a practical **agentic AI workflow for LinkedIn content generation**.

The system demonstrates:

* AI content generation
* AI agent orchestration
* Web research
* Tool calling
* AI-based content review
* Automatic revision
* Stateful workflows
* Conditional routing
* Local LLM execution

---

# ✨ Features

## 📝 1. LinkedIn Post Generation

The Writer Agent generates a professional LinkedIn post based on a topic.

The Writer follows rules such as:

* Strong hook in the first line
* One clear takeaway
* Short paragraphs
* Easy-to-read structure
* Professional but human tone
* Approximately 150–200 words
* Ends with a question or call-to-action
* No unnecessary hashtags

---

## 🔎 2. Web Research

The project integrates **Tavily Search**.

When current information, statistics, trends, or recent developments are required, the Writer Agent can call the search tool.

```text
Topic
  ↓
Writer Agent
  ↓
Need Current Information?
  ↓
Tavily Search
  ↓
Search Results
  ↓
Writer Agent
  ↓
Final Draft
```

---

## 🤖 3. AI Reviewer

After generating a draft, the Reviewer Agent evaluates it.

The Reviewer checks:

```text
✓ Strong hook
✓ Clear takeaway
✓ Easy to skim
✓ Approximately 150–200 words
✓ Engaging ending
✓ Professional human tone
✓ No hashtags
```

The Reviewer returns:

```text
VERDICT: APPROVED
FEEDBACK: The post meets the required criteria.
```

or:

```text
VERDICT: REJECTED
FEEDBACK: The opening needs a stronger hook.
```

---

# 🔄 4. Automatic Revision Loop

If the Reviewer rejects the draft, the feedback is automatically sent back to the Writer.

```text
Writer
  ↓
Draft
  ↓
Reviewer
  ↓
Rejected
  ↓
Feedback
  ↓
Writer
  ↓
Improved Draft
  ↓
Reviewer
```

The current workflow allows a maximum of **3 attempts**.

This prevents the graph from entering an infinite loop.

---

# 🧠 LangGraph Workflow

The project uses the following LangGraph nodes:

| Node            | Responsibility                          |
| --------------- | --------------------------------------- |
| `writer`        | Generates or rewrites the LinkedIn post |
| `tools`         | Executes Tavily web search              |
| `extract_draft` | Extracts the generated post             |
| `reviewer`      | Reviews and approves/rejects the draft  |

### Workflow

```text
                         START
                           │
                           ▼
                    ┌─────────────┐
                    │    WRITER   │
                    │   Ollama    │
                    └──────┬──────┘
                           │
                    Tool call required?
                       /         \
                     YES          NO
                      │            │
                      ▼            │
               ┌─────────────┐    │
               │    TOOLS    │    │
               │   Tavily    │    │
               └──────┬──────┘    │
                      │            │
                      └─────┬──────┘
                            ▼
                   ┌────────────────┐
                   │ EXTRACT DRAFT  │
                   └───────┬────────┘
                           │
                           ▼
                   ┌───────────────┐
                   │    REVIEWER   │
                   │    Ollama     │
                   └───────┬───────┘
                           │
                    ┌──────┴──────┐
                    │             │
                 APPROVED       REJECTED
                    │             │
                    ▼             ▼
                   END         Feedback
                                  │
                                  ▼
                               WRITER
```

---

# 🦙 Using Ollama

This project uses **Ollama** to run the LLM locally.

The advantage is that the main LLM does not need a cloud API key or cloud request quota.

## 1. Install Ollama

Install Ollama for Windows.

Verify the installation:

```powershell
ollama --version
```

---

## 2. Download an AI Model

For example:

```powershell
ollama pull llama3.2
```

Check installed models:

```powershell
ollama list
```

---

## 3. Test Ollama

Run:

```powershell
ollama run llama3.2
```

Then enter:

```text
Write a LinkedIn post about Artificial Intelligence.
```

Exit the model:

```text
/bye
```

---

# 🐍 Python + Ollama

Install the LangChain Ollama integration:

```powershell
pip install -U langchain-ollama
```

Use Ollama in Python:

```python
from langchain_ollama import ChatOllama

writer_llm = ChatOllama(
    model="llama3.2",
    temperature=0.7,
)

reviewer_llm = ChatOllama(
    model="llama3.2",
    temperature=0.2,
)
```

The Writer can use tools:

```python
writer_llm_with_tools = writer_llm.bind_tools(tools)
```

---

# 🔎 Tavily Setup

Tavily is used for web search.

Install:

```powershell
pip install -U langchain-tavily
```

Create a `.env` file:

```env
TAVILY_API_KEY=your_tavily_api_key
```

Load environment variables:

```python
from dotenv import load_dotenv

load_dotenv()
```

Create the search tool:

```python
from langchain_tavily import TavilySearch

search_tool = TavilySearch(
    max_results=3
)

tools = [search_tool]
```

---

# 📦 Installation

## 1. Clone the Repository

```powershell
https://github.com/SubhasishElixor-HQ/langgraph-agents.git
```

Move into the project:

```powershell
cd langgraph-agents
```

---

## 2. Create a Virtual Environment

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\Activate.ps1
```

If PowerShell activation is unavailable, use:

```powershell
.venv\Scripts\activate
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

Or install them manually:

```powershell
pip install -U langchain
pip install -U langgraph
pip install -U langchain-ollama
pip install -U langchain-tavily
pip install -U python-dotenv
```

---

# 🔐 Environment Variables

Create:

```text
.env
```

Add:

```env
TAVILY_API_KEY=your_tavily_api_key
```

Do **not** commit `.env` to GitHub.

Add the following to `.gitignore`:

```text
.env
.venv/
__pycache__/
*.pyc
```

---

# ▶️ How to Run the Project

## Step 1 — Start Ollama

Check that Ollama is available:

```powershell
ollama list
```

If the required model is not installed:

```powershell
ollama pull llama3.2
```

---

## Step 2 — Activate Virtual Environment

```powershell
.venv\Scripts\activate
```

---

## Step 3 — Run the Python Application

If your main file is `main.py`:

```powershell
python main.py
```

---

# 💻 Example

### Input

```text
Enter topic:
How AI is changing software development
```

### Processing

```text
[Writer] Generating draft...

[Writer] Searching web using Tavily...

[Writer] Generating final draft...

[Reviewer] Reviewing draft...

[Verdict: REJECTED]

[Writer] Revising draft...

[Reviewer] Reviewing revised draft...

[Verdict: APPROVED]
```

### Output

```text
Final LinkedIn Post
────────────────────────────

AI is changing software development faster
than most developers expected.

...

What part of software development do you
think AI will transform next?
```

---


# 🗂️ State Management

LangGraph maintains the application state using:

```python
class State(TypedDict):
    topic: str
    messages: Annotated[list, add_messages]
    draft: str
    review_feedback: str
    is_approved: bool
    attempt: int
```

### State Fields

| Field             | Description                |
| ----------------- | -------------------------- |
| `topic`           | User's requested topic     |
| `messages`        | LLM and tool messages      |
| `draft`           | Current LinkedIn post      |
| `review_feedback` | Feedback from Reviewer     |
| `is_approved`     | Approval status            |
| `attempt`         | Number of writing attempts |

---

# 🛠️ Technologies

| Technology    | Purpose                      |
| ------------- | ---------------------------- |
| Python        | Programming language         |
| LangChain     | LLM and tool integration     |
| LangGraph     | Agent workflow orchestration |
| Ollama        | Local LLM execution          |
| Tavily        | Web research                 |
| python-dotenv | Environment configuration    |
| Git           | Version control              |
| GitHub        | Source-code hosting          |
| VS Code       | Development environment      |

---

# 🧠 What I Learned

This project helped me understand and implement:

* LangChain
* LangGraph
* AI agents
* Stateful AI workflows
* Tool calling
* Web search integration
* Prompt engineering
* AI evaluation
* Feedback loops
* Conditional graph routing
* Local LLMs with Ollama
* Environment variables
* Python virtual environments
* Git and GitHub
* Agentic AI architecture

---

# 🚧 Current Limitations

* LinkedIn publishing is not automated.
* Tavily requires an external API key.
* Local LLM performance depends on available CPU, GPU, RAM, and model size.
* Generated content should still be reviewed by a human before publishing.
* Tool-calling capabilities depend on the selected Ollama model.
* The current project focuses on generating text rather than complete social-media management.

---

# 🔮 Future Improvements

## AI Improvements

* Research Agent
* Fact-Checking Agent
* Multiple Writer Agents
* Advanced Reviewer Agent
* Personal writing-style adaptation
* RAG-based content generation
* Long-term memory
* Content quality scoring

## Content Features

* Technical LinkedIn posts
* Educational posts
* Storytelling posts
* Founder posts
* Career posts
* LinkedIn carousel generation
* LinkedIn article generation

## Product Features

* Web dashboard
* User authentication
* Saved drafts
* Post history
* Content calendar
* Analytics
* Scheduled publishing
* Multi-platform content generation

---

# 🔮 Future Agent Architecture

```text
                         USER
                           │
                           ▼
                    ┌──────────────┐
                    │    TOPIC     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   RESEARCH   │
                    │    AGENT     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │    WRITER    │
                    │    AGENT     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │ FACT CHECKER │
                    │    AGENT     │
                    └──────┬───────┘
                           │
                           ▼
                    ┌──────────────┐
                    │   REVIEWER   │
                    │    AGENT     │
                    └──────┬───────┘
                           │
                     Approved?
                      /       \
                    YES        NO
                     │          │
                     ▼          ▼
                   FINAL      WRITER
                   POST         │
                                └──────► Review
```

---

# 📈 Project Vision

The long-term vision is to evolve this project from a simple LinkedIn post generator into an **AI-powered content workflow system** capable of:

```text
Research
   ↓
Generate
   ↓
Fact Check
   ↓
Review
   ↓
Improve
   ↓
Verify
   ↓
Publish
```

The project demonstrates how multiple AI capabilities can be combined into a controlled, stateful, and iterative workflow using **LangGraph**.

---

# 👨‍💻 Author

## Subhasish Sahoo

**B.Tech CSE — Artificial Intelligence & Machine Learning**

### Interests

```text
Artificial Intelligence
Machine Learning
Generative AI
LLMs
RAG
AI Agents
LangGraph
LangChain
FastAPI
Backend Development
```

---

# ⭐ Project

If you find this project useful, consider giving the repository a ⭐ on GitHub.

---