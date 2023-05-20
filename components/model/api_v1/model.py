from pydantic import BaseModel

class TrainedModel(BaseModel):
    id: str
    name: str
    author: Optional[str]
    version: float
