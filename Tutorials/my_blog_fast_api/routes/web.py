from fastapi import HTTPException, Request, status, APIRouter
from config import templates
from data.blog_entries import posts, blog_name, about

data = {"posts": posts, "title": blog_name}

# -------------------------------- HTML Routes --------------------------------

router = APIRouter()


@router.get("/", include_in_schema=False, name="home")
@router.get("/posts", include_in_schema=False, name="posts")
def home(request: Request):
    return templates.TemplateResponse(request, "home.html", data)


@router.get("/posts/{post_id}", include_in_schema=False, name="post_detail")
def get_post_page(request: Request, post_id: int):
    for post in posts:
        if post.get("id") == post_id:
            return templates.TemplateResponse(
                request, "post.html", {"post": post, "title": data["title"]}
            )
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")


@router.get("/about", include_in_schema=False, name="about")
def about_page(request: Request):
    return templates.TemplateResponse(
        request, "about.html", {"about": about, "title": data["title"]}
    )
