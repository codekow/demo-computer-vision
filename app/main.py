#!/usr/bin/env python
# https://stackoverflow.com/questions/1523427/what-is-the-common-header-format-of-python-files

from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.responses import HTMLResponse

import markdown

def create_app():
    app = FastAPI()

    @app.get(
    "/", 
    response_class=HTMLResponse,
    summary="General Info",
    )
    def root():
        with open("README.md", "r") as f:
            index = f.read()
            html = markdown.markdown(index)
            response = "<HTML>\n" + html + "\n</HTML>"
            return response

    import api_v1.healthz
    import api_v1.detect
    # import api_v1.example

    app.include_router(api_v1.healthz.app)
    app.include_router(api_v1.detect.app, prefix="/v1", tags=["latest"])
    # app.include_router(api_v1.example.app, prefix="/v1", tags=["latest"])

    return app


app = create_app()

# uvicorn main:app --host 0.0.0.0 --port 8080 --reload
if __name__ == "__main__":

    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8080, log_level="debug")
