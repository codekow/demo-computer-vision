from pydantic import BaseModel

class TrainedModel(BaseModel):
    id: str
    name: str
    author: str
    version: float
    genre: str

