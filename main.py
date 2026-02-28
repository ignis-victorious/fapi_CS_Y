#
#  Import FILES
from fastapi import FastAPI, Request

# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.templating import _TemplateResponse  # type: ignore

#  Import LIBRARIES
from data.posts import posts

#
#  _______________________

app = FastAPI()

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="./templates")


@app.get(path="/", include_in_schema=False, name="home")
@app.get(path="/posts", include_in_schema=False, name="posts")
def home(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(request=request, name="home.html", context={"posts": posts, "title": "Home"})


# @app.get(path="/", response_class=HTMLResponse, include_in_schema=False)
# @app.get(path="/posts", response_class=HTMLResponse, include_in_schema=False)
# def home() -> str:
#     return f"<h1›{posts[0]['title']}</h1>"


# @app.get(path="/", include_in_schema=False)
# @app.get(path="/posts", include_in_schema=False)
# def home(request: Request) -> _TemplateResponse:
#     return templates.TemplateResponse(request=request, name="home.html")


# @app.get(path="/", response_class=HTMLResponse, include_in_schema=False)
# @app.get(path="/posts", response_class=HTMLResponse, include_in_schema=False)
# def home() -> str:
#     return f"<h1>{posts[0]['title']}</h1>"
# @app.get(path="/", response_class=HTMLResponse)
# def home() -> dict[str, str]:
# return {"message": "Hello World"}


@app.get(path="/api/posts")
def get_posts() -> list[dict[str, int | str]]:
    return posts
