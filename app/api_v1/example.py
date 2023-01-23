from fastapi import APIRouter
#from model.detect_v1 import Detect

app = APIRouter(
    prefix="/example",
    tags=["v1"],
    responses={404: {"description": "Not found"}},
)


@app.get("")
def smoke_test():
    return "ok"
