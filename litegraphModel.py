from collections import namedtuple
from typing import Any, List, Mapping, Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel, Json
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse, RedirectResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware


class Litegraph(BaseModel):
    @classmethod
    def make(cls, raw_json):
        model = Litegraph.parse_raw(raw_json)
        model.raw_json = raw_json

        return model

    class Node(BaseModel):
        class Input(BaseModel):
            name: str
            type: str
            link: Optional[int]

        class Output(BaseModel):
            name: str
            type: str
            links: Optional[List[int]]

        id: int
        type: str
        inputs: Optional[List[Input]]
        outputs: Optional[List[Output]]
        properties: Mapping[str, Any]

    Link = namedtuple("Link", ["id", "in_node", "in_id", "out_node", "out_id", "type"])

    raw_json: Optional[str]

    nodes: List[Node]
    links: List[Link]
    # TODO: What is format of `links`?, Are `groups` in scope?, What is `config`?


app = Starlette(debug=True)

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])

static_root = "/home/daniel/git/litegraph.js/"
app.mount("/css", StaticFiles(directory=static_root + "css"), "css")
app.mount("/js", StaticFiles(directory=static_root + "demo/js"), "css")
app.mount("/src", StaticFiles(directory=static_root + "src"), "src")
app.mount("/external", StaticFiles(directory=static_root + "external"), "external")
app.mount("/demo", StaticFiles(directory=static_root + "demo"), "demo")
# app.mount("/", StaticFiles(directory=static_root + "demo"), "root")


@app.route("/")
def index(request):
    return RedirectResponse("/demo/index.html")


state: List[Litegraph] = [None]


@app.route("/api/restore", methods=["GET"])
def restore(request: Request):
    if state[0] is None:
        return PlainTextResponse("Bad", status_code=404)
    return PlainTextResponse(state.raw_json)


@app.route("/api/save", methods=["POST"])
async def save(request: Request):
    json = await request.body()  # returns bytes, not dict
    global state
    print(json)
    state[0] = Litegraph.make(json)

    return info(request)


@app.route("/api/info", methods=["GET"])
def info(request: Request):
    data = {"saved": (state[0] is not None)}
    if not data["saved"]:
        return JSONResponse(data)

    data["node_count"] = len(state[0].nodes)

    return JSONResponse(data)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app)
