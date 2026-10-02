import os
from typing import TypedDict

# create stae
class  pipelinestate(TypedDict):
    raw_input : str
    edited_text : str 
    script_text: str
    final_output : str

from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from dotenv import load_dotenv
load_dotenv()

# 2. Create Hugging Face LLM
llm = HuggingFaceEndpoint(
    repo_id="deepseek-ai/DeepSeek-R1-0528",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

# create node
def editer_node(state: pipelinestate) -> dict:
    """stage 1 cleans up grammer, remove typos,and defines the tone of the text"""

    prompt = f"""
    You are a professional editor. Your task is to clean up the grammar, remove typos, and define the tone of the text. 
    Please provide a polished version of the following text:

    {state['raw_input']}

    Please ensure that the edited text maintains the original meaning and context.
    """
    response = model.invoke(prompt)
    return{
        "edited_text": response.content.strip()
    }


# second node
def scriptwriter_node(state: pipelinestate) -> dict:
    """stage 2 converts the text into a script format suitable for video production"""

    prompt = f"""
    You are a professional scriptwriter. Your task is to convert the following text into a script format suitable for video production. 
    Please provide a well-structured script that includes scene descriptions, dialogues, and any necessary instructions for the actors.

    {state['edited_text']}

    Please ensure that the script is engaging and maintains the original meaning and context of the text.
    """
    response = model.invoke(prompt)
    return{
        "script_text": response.content.strip()
    }

# third node
def translator_node(state: pipelinestate) -> dict:
    """stage 3 translates the script into a specified language while preserving the original meaning and context"""

    prompt = f"""
    You are a professional translator. Your task is to translate the following script into a specified language while preserving the original meaning and context. 
    Please provide an accurate and culturally appropriate translation of the script.

    {state['script_text']}

    Please ensure that the translated script maintains the original tone, style, and intent of the text.
    """
    response = model.invoke(prompt)
    return{
        "final_output": response.content.strip()
    }

# nowyour state and nodes are ready to be used in a graph. You can create a graph using the state and nodes defined above, and then execute the graph to process the input text through the different stages of editing, scriptwriting, and translation.
# connect and edges ate very important in graph. You can connect the nodes using edges to define the flow of data between them. For example, you can connect the output of the editer_node to the input of the scriptwriter_node, and then connect the output of the scriptwriter_node to the input of the translator_node. This way, the data will flow through the different stages of processing in a sequential manner.

# create graph
from langgraph.graph import StateGraph, START, END
graph = StateGraph(pipelinestate)

# add nodes to graph
graph.add_node("editer_node", editer_node)
graph.add_node("scriptwriter_node", scriptwriter_node)
graph.add_node("translator_node", translator_node)

# add edges to graph
graph.add_edge(START, "editer_node")
graph.add_edge("editer_node", "scriptwriter_node")
graph.add_edge("scriptwriter_node", "translator_node")
graph.add_edge("translator_node", END)

# compile graph
app = graph.compile()
result = app.invoke({
    "raw_input": "This is a sample text that needs to be edited, converted into a script, and translated into another language."
})

# output the final result
print("your final output is:- \n\n")
print(result["final_output"])