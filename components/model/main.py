#!/usr/bin/env python
# https://stackoverflow.com/questions/1523427/what-is-the-common-header-format-of-python-files

from fastapi import FastAPI, APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, FileResponse

from markdown import markdown
import markdown.extensions.fenced_code


def render_markdown(file):
    """Render Markdown Syntax to final HTML."""
    with open(file, "r") as input_file:
        text = input_file.read()
        input_file.close()

        rendered = markdown.markdown(text, extensions=["fenced_code", "codehilite"])
        html = "<html>\n" + rendered + "\n</html>"

    return html


def create_app():
    app = FastAPI()
    favicon_path = "favicon.ico"

    @app.get(
        "/",
        response_class=HTMLResponse,
        summary="General Info",
    )

    # @app.get("/favicon.ico", include_in_schema=False)
    # async def favicon():
    #     return FileResponse(favicon_path)

    def root():
        return render_markdown("README.md")

    import healthz
    import api_v1.detect
    import api_v1.file

    # import api_v1.example

    app.include_router(healthz.app)
    app.include_router(api_v1.detect.app, prefix="/v1", tags=["latest", "v1"])
    app.include_router(api_v1.file.app, prefix="/v1", tags=["latest", "v1"])
    # app.include_router(api_v1.example.app, prefix="/v1", tags=["latest"])

    return app


app = create_app()

if __name__ == "__main__":

    # Use this for debugging purposes only
    import uvicorn

    # uvicorn main:app --host 0.0.0.0 --port 8080 --reload
    # uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
    uvicorn.run("main:app", port=8080, reload=True)
