#class for common functions
from fastapi.responses import JSONResponse
from fastapi import FastAPI, status, HTTPException
from collections.abc import Iterable

class CommonFxn:
    """#check if object is iterable but not string
    def is_iterable(self,obj):
        return isinstance(obj, Iterable) and not isinstance(obj, (str, bytes))
    
    #convert response to json and return
    def responseToJSON(self,model,result):
        if not self.is_iterable(result):
            print('iera')
            resp = model.model_validate(result).model_dump() 
        else:
            print('im iterable but no iterable')
            resp = [model.model_validate(res).model_dump() for res in result]
        return JSONResponse(content=resp, status_code=status.HTTP_200_OK)
        """
    pass