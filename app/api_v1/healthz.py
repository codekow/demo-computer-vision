from fastapi import APIRouter

app = APIRouter(
    prefix="/healthz",
)


@app.get(
    "",
    summary="Generic Health Check",
    description="This entrypoint is used to check if the service is alive or dead.",
    status_code=204,
    response_model=None,
    tags=["healthz"],
    # include_in_schema=False
)

def healthz_ok():
    return {"status": 200, "title": "OK"}

@app.get(
    "/live",
    summary="Kubernetes Liveliness Check",
    description="This entrypoint is used to check if the service is alive in k8s",
    status_code=200,
    response_model=None,
    tags=["healthz"],
    # include_in_schema=False
)
def liveness():
    return healthz_ok()

@app.get(
    "/ready",
    summary="Kubernetes Readiness Check",
    description="This entrypoint is used to check if the service is ready in k8s",
    status_code=200,
    response_model=None,
    tags=["healthz"],
    # include_in_schema=False
)
def readiness():
    try:
        check_model()
    except Exception as e:
        print(e)
        return { "message": "error"}
    
    return healthz_ok()
