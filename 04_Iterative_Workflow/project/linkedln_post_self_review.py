import os 
from typing import TypedDict, Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama
from langchain_tavily import TavilySearch
from dotenv import load_dotenv


load_dotenv()

#tools 

search_tool = TavilySearch(max_results = 3)


tools = [search_tool]

#llms 

#writer
writer_llm = ChatOllama(
    model="llama3.2",
    temperature=0.7,
)


writer_llm_with_tools = writer_llm.bind_tools(tools)

#reviewer

reviewer_llm = ChatOllama(
    model="llama3.2",
    temperature=0.2,
)

#state building 

class State(TypedDict):
    topic : str 
    messages : Annotated[list,add_messages]
    draft : str 
    review_feedback : str
    is_approved : bool 
    attempt : int


#nodes 

WRITER_SYSTEM_PROMPT = (
    "You are an expert LinkedIn content writer. Your job is to write "
    "engaging, professional LinkedIn posts about the given topic. "
    "If the topic requires up-to-date information, statistics, or "
    "current trends, use the web search tool to gather fresh context "
    "before writing. If you have already received feedback on a "
    "previous draft, carefully address every point in the new draft. "
    "Rules for good LinkedIn posts: strong hook in the first line, "
    "1 clear takeaway, easy to skim (short paragraphs), around "
    "150–200 words, ends with a question or call-to-action to invite "
    "engagement. Do not use hashtags."
)


def writer_node(state : State) -> dict:
    """Writes (or rewrites) the LinkedIn post. Can call Tavily to search first."""
    attempt = state.get("attempt",0) + 1 
    topic = state["topic"]
    previous_feedback = state['review_feedback']

    if attempt == 1:
        user_message = (
            f"Write a LinkedIn post on this topic {topic}"
            f"if you need current info search the web first "
        )
    else:
        user_message = (
            f"your previous draft on '{topic}' was rejected"
            f"Here is the reviewer's feedback \n\n {previous_feedback}\n\n"
            f"Write a new, improved draft that fixes every issue mentiond"
            f"do not repeat the same mistake"
        )
    messages = [("system",WRITER_SYSTEM_PROMPT),("human",user_message)]
    response = writer_llm_with_tools.invoke(messages)

    return {
        "messages" : [("human",user_message),response],
        "attempt" : attempt
    }

tool_node = ToolNode(tools)

def extract_draft_node(state:State) -> dict:
    """After the writer finishes tool calls, pulls the final text out as the draft."""
    last_message = state['messages'][-1]
    draft = last_message.content 
    print(f"\n\n generated post \n {draft} \n ")
    return {"draft" : draft}
    

REVIEWER_SYSTEM_PROMPT = (
    "You are a strict LinkedIn content reviewer. You judge whether a "
    "post is publish-ready. Evaluate against these criteria:\n"
    "1. Strong hook in the first line\n"
    "2. One clear, valuable takeaway\n"
    "3. Easy to skim — uses short paragraphs\n"
    "4. Roughly 150-200 words\n"
    "5. Ends with an engaging question or CTA\n"
    "6. Professional but human tone (not corporate-robotic)\n"
    "7. No hashtags\n\n"
    "Respond in exactly this format:\n"
    "VERDICT: APPROVED or REJECTED\n"
    "FEEDBACK: <one short paragraph explaining why>\n\n"
    "Be strict but fair. Approve only if the post genuinely meets all "
    "criteria. Reject if even one criterion is clearly missing."
)

def reviewer_node(state: State) -> dict:
    """Reviews the LinkedIn post without using another LLM/API."""

    draft = state.get("draft", "").strip()

    if not draft:
        return {
            "review_feedback": "Draft is empty. Generate a complete post.",
            "is_approved": False,
        }

    feedback = []

    # 1. Word count
    words = draft.split()
    word_count = len(words)

    if word_count < 150:
        feedback.append(
            f"Post is too short ({word_count} words). Aim for 150-200 words."
        )

    elif word_count > 200:
        feedback.append(
            f"Post is too long ({word_count} words). Keep it around 150-200 words."
        )

    # 2. Hook
    first_line = draft.split("\n")[0].strip()

    if len(first_line) < 15:
        feedback.append(
            "The opening hook is too weak. Start with a stronger first line."
        )

    # 3. CTA / question
    if not draft.rstrip().endswith(("?", ".", "!")):
        feedback.append(
            "End the post with a clear question or call-to-action."
        )
    elif "?" not in draft and not any(
        phrase in draft.lower()
        for phrase in [
            "comment",
            "share",
            "let me know",
            "what do you think",
            "try this",
            "follow",
        ]
    ):
        feedback.append(
            "Add an engaging question or clear call-to-action at the end."
        )

    # 4. Hashtags
    if "#" in draft:
        feedback.append(
            "Remove hashtags. The post should not contain hashtags."
        )

    # 5. Very long paragraphs
    paragraphs = [
        p.strip()
        for p in draft.split("\n\n")
        if p.strip()
    ]

    for paragraph in paragraphs:
        if len(paragraph.split()) > 70:
            feedback.append(
                "Break long paragraphs into shorter, easier-to-skim sections."
            )
            break

    # --------------------------------
    # Verdict
    # --------------------------------

    if feedback:
        is_approved = False
        review_feedback = " ".join(feedback)
        verdict = "REJECTED"
    else:
        is_approved = True
        review_feedback = (
            "The post meets the basic LinkedIn content requirements."
        )
        verdict = "APPROVED"

    print(f"\n[Verdict: {verdict}]")
    print(f"[Feedback: {review_feedback}]\n")

    return {
        "review_feedback": review_feedback,
        "is_approved": is_approved,
    }

#router function 

def should_use_tool(state:State):
    last_message = state['messages'][-1]

    if getattr(last_message,'tool_calls',None):
        return "tools"
    return "extract_draft"

def should_stop_looping(state:State):
    if state['is_approved']:
        print("post haas been approved \n")
        return END
    if state['attempt'] >= 3:
        print("reached max attempts")
        return END 
    return "writer"

#build the graph 
graph = StateGraph(State)

graph.add_node("writer",writer_node)
graph.add_node("tools",tool_node)
graph.add_node("extract_draft",extract_draft_node)
graph.add_node("reviewer",reviewer_node)

graph.add_edge(START,"writer")

graph.add_conditional_edges(
    "writer",should_use_tool,
)

graph.add_edge("tools","writer")
graph.add_edge("extract_draft", "reviewer")

graph.add_conditional_edges(
    "reviewer",should_stop_looping
)

app = graph.compile()


print("=" * 55)
print("Welcome to the LinkedIn Post Generator")
print("=" * 55)
print("\nThis tool will draft a LinkedIn post for you, review it")
print("itself, and iterate until it's publish-ready.")

print("=" * 55)

topic = input("\nWhat topic do you want a LinkedIn post about?\n> ").strip()

if not topic:
    print("\nNo topic given. Exiting.")
else:
    print("\nStarting generation...\n")

    initial_state = {
        "topic": topic,
        "messages": [],
        "draft": "",
        "review_feedback": "",
        "is_approved": False,
        "attempt": 0,
    }

    final_state = app.invoke(initial_state)

    print("\n" + "=" * 55)
    print("FINAL LINKEDIN POST")
    print("=" * 55)
    print(final_state["draft"])
    print("=" * 55)
    print(f"Total attempts: {final_state['attempt']}")
    print(f"Approved: {final_state['is_approved']}")