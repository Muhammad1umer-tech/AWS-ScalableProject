from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from fastapi import FastAPI

from local import input_to_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Change to specific origins if needed.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods.
    allow_headers=["*"],  # Allows all headers.
)

class Item(BaseModel):
    input: str
    
# @app.post("/createDatabase/", )
# async def createDatabase():
#     result = create_database()
#     return JSONResponse(content={"message": result}, status_code=200)

# POST endpoint to create a new item
@app.post("/inputToResponse", response_model=Item)
async def inputToResponse(item: Item):
    result = input_to_response(item.input)
    return JSONResponse(content={"message": result}, status_code=200)


@app.get("/test")
async def test():
    return {"message": "Hello world"}
