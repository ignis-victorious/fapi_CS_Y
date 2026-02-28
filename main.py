#
#  Import LIBRARIES
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.templating import _TemplateResponse  # type: ignore

#  Import FILES
from data.posts import posts
from models.models import Post

#
#  _______________________
#

app = FastAPI()

app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="./templates")


@app.get(path="/", include_in_schema=False, name="home", response_model=None)
@app.get(path="/posts", include_in_schema=False, name="posts")
def home(request: Request) -> _TemplateResponse:
    return templates.TemplateResponse(request=request, name="home.html", context={"posts": posts, "title": "Home"})


@app.get(path="/posts/{post_id}", include_in_schema=False, response_model=None)
def post_page(request: Request, post_id: int) -> _TemplateResponse | None:
    for post in posts:
        if post.get("id") == post_id:
            title: int | str = post["title"[:50]]
            return templates.TemplateResponse(
                request=request,
                name="post.html",
                context={"post": post, "title": title},
            )
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@app.get(path="/api/posts", response_model=list[Post])
def get_posts() -> list[dict[str, int | str]]:
    return posts


# @app.get(path="/api/posts/{posts_id}", response_model=Post, status_code=200)
# def get_post(posts_id: int) -> dict[str, int | str]:
#     # 'next' finds the first match or returns None if it's empty
#     post: dict[str, int | str] | None = next((p for p in posts if p.get("id") == posts_id), None)

#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

# return post


@app.get(path="/api/posts/{posts_id}")
def get_post(posts_id: int) -> dict[str, int | str] | dict[str, str]:
    for post in posts:
        if post.get("id") == posts_id:
            return post
    return {"error": "post not found"}


## StarletteHTTPException Handler
@app.exception_handler(exc_class_or_status_code=StarletteHTTPException)
def general_http_exception_handler(
    request: Request, exception: StarletteHTTPException
) -> JSONResponse | _TemplateResponse:
    message: str = (
        exception.detail if exception.detail else "An error occurred. Please check your request and try again."
    )

    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=exception.status_code,
            content={"detail": message},
        )
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "status_code": exception.status_code,
            "title": exception.status_code,
            "message": message,
        },
        status_code=exception.status_code,
    )


### RequestValidationError Handler
@app.exception_handler(exc_class_or_status_code=RequestValidationError)
def validation_exception_handler(
    request: Request, exception: RequestValidationError
) -> JSONResponse | _TemplateResponse:
    if request.url.path.startswith("/api"):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            content={"detail": exception.errors()},
        )
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "status_code": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "title": status.HTTP_422_UNPROCESSABLE_CONTENT,
            "message": "Invalid request. Please check your input and try again.",
        },
        status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
    )
