from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional

app = APIRouter(
    prefix="/example",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)

class Model(BaseModel):
    name: str
    description: str
    version: Optional[float]

@app.post("", response_model=Model)
async def echo(model: Model):
    return model
