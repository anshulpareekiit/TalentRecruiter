from fastapi import FastAPI, status, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.utils.responseSchema import ResponseSchema

# Custom handler for HTTPException (normal raise HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    content = ResponseSchema(
        success=False,
        status_code=exc.status_code,
        message=str(exc.detail),
        data={}
    ).model_dump(mode='json')
    return JSONResponse(content=content, status_code=exc.status_code)

# Custom handler for Validation Error
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    content = ResponseSchema(
        success=False,
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        message="Validation Errorssss",
        data=exc.errors()   # returns the list of validation errors
        
    ).model_dump(mode='json')
    return JSONResponse(content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)

def success_response(message: str, data:dict = None, status_code: int = status.HTTP_200_OK):
    """
    Customize and return a success response.
    """
    print(message)
    content = ResponseSchema(
        success = True,
        message = message,
        data = data if data else {},
        status_code = status_code
    )
    
    return _generate_response(content)

def _generate_response(content):
    """
    Standardize the response format.
    """
    response = {
        "success":  content.success,
        "message": content.message,
        "data": content.data
        }
    return JSONResponse(content=response, status_code=content.status_code)
