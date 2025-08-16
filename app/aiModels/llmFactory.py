#importing groq LLM If you have other lLM then import them

'''
Description:    factory which will return LLM Object as per provider
created By:     Anshul Pareek
date:           16-Aug-25 17:06:26 PM IST
'''
 
from app.aiModels.groqReqRes import GroqLLM
'''
Desc: Returning OBJECT for LLM given as parameter(Provider)
'''
class LLMFactory:
    def getLLm(provider: str):
        if provider == 'groq':
            return GroqLLM()
        else:
            raise ValueError(f"Unsupported provider: {provider}")

