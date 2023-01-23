from pydantic import BaseModel

class TrainedModel(BaseModel):
    id: str
    name: str
    author: str
    publication_year: int
    genre: str
