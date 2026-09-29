import os 

#1) typed DICT (Most common approach)

from typing import TypedDict

class State(TypedDict):
    topic : str
    summary : str 
    score : int 


#2) pydantic approach 
#it is good at data validation and type checking at 
#runtime 

from pydantic import BaseModel, field_validator

class State(BaseModel):
    topic : str 
    score :int 
    summary : str = ""

    @field_validator
    def score_positive(cls,v):
        if v < 0:
            raise ValueError("score must be positive")

#3)python dataclaseess 

#standard python dataclass but it is used very rarelty 

from dataclasses import dataclass, field 

@dataclass
class State:
    topic : str = ""
    summary  : str = ""
    messages : list = field(default_factory=list)

# 4) langgraph approach
from langgraph.graph import MessagesState

class State(MessagesState):
    # messages field is already included with add_messages reducer
    # just add your extra fields
    user_name: str
    language: str