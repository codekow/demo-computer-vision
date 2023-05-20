from fastapi import APIRouter, HTTPException

app = APIRouter(
    prefix="/healthz",
    tags=["healthz"],
    # include_in_schema=False
)

@app.get(
    "",
    summary="Generic Health Check",
    description="This entrypoint is used to check if the service is alive or dead.",
    status_code=204,
    response_model=None,
)
def healthz_ok():
    return {"status": 200, "title": "OK"}

@app.get(
    "/live",
    summary="Kubernetes Liveliness Check",
    description="This entrypoint is used to check if the service is alive in k8s",
)
def liveness():
    return healthz_ok()

@app.get(
    "/ready",
    summary="Kubernetes Readiness Check",
    description="This entrypoint is used to check if the service is ready in k8s",
)
def readiness():
    try:
        find_camera_ready()
    except Exception as e:
        raise HTTPException(
            status_code=503, detail=f"{str(e)}"
        )
    return healthz_ok()
