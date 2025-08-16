#this is an abstract class which needs to be implemented by the child class
from abc import ABC, abstractmethod
from typing import List,Dict

class BaseLLM(ABC):
    @abstractmethod
    async def chat(self, messages:List[Dict], model: str)->Dict:
        pass
    