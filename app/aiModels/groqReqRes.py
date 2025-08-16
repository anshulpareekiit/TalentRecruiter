'''
Description: To send request for GROQ LLM and receives the response
Inheritance: BaseLLM inherited to implement bareminimum
'''
import httpx
from app.core.config import settings
from app.aiModels.base import BaseLLM
from typing import List,Dict
from groq import Groq
import json

class GroqLLM(BaseLLM):
    
    client = Groq()
    async def chat(self, messages):
        completion = self.client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=messages,
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            reasoning_effort="medium",
            stream=False,
            response_format={"type": "json_object"},
            stop=None,
            tools=[]
        )
        print(completion);
        return json.loads(completion.choices[0].message.content)
    
    async def chat1(self, messages, model='mixtral-8x7b-32768'):
        try:
            headers = {
                "Authorization": f"Bearer {settings.GROQ_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {"model": model, "messages": messages}
            async with httpx.AsyncClient() as client:
                response = await client.post(settings.GROQ_API_URL, json=payload, headers=headers)
                response.raise_for_status()
                print('response::::')
                print(response)
                return response.json()
        except Exception as e:
            print('error:::::')
            print(e)