'''
Description: This controller used to call the LLM API.
'''
#NOT USING ANYWHERE WILL UTILIZE IN FUTURE
from fastapi import APIRouter, HTTPException
from app.api.v1.llmCall.llmCallModel import LLMRequest
from app.aiModels.llmFactory import LLMFactory

router = APIRouter(prefix="/llm", tags=["LLM"])

#returning LLM Object as per the provider
getLLM = LLMFactory()
'''
Description: this is internal call method means called by other methods of other services
USAGE: Call if you want to make call to LLM and provide the llm name default is Grouq
'''
@router.post("/chat")
async def chat(request: LLMRequest):
    try:
        llmObj = getLLM.getLLm(request.provider) #Selecting LLM to be called (groq etc)
        result = await llmObj.chat([msg.model_dump() for msg in request.messages], request.model)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
