from pydantic import BaseModel
from typing import List
'''Type of parameters needs to be sent in message'''
class Message(BaseModel):
    role: str
    content: str

'''LLM Request Parameters specified'''
class LLMRequest(BaseModel):
    provider: str  # "groq", "openai", etc.
    model: str
    messages: List[Message]
