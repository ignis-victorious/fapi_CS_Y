#
#  Import FILES
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

#  Import LIBRARIES
from data.posts import posts

#
#  _______________________

app = FastAPI()


@app.get(path="/", response_class=HTMLResponse, include_in_schema=False)
@app.get(path="/posts", response_class=HTMLResponse, include_in_schema=False)
def home() -> str:
    return f"<h1>{posts[0]['title']}</h1>"


# @app.get(path="/", response_class=HTMLResponse)
# def home() -> dict[str, str]:
# return {"message": "Hello World"}


@app.get(path="/api/posts", response_class=HTMLResponse)
def get_posts() -> list[dict[str, int | str]]:
    return posts
