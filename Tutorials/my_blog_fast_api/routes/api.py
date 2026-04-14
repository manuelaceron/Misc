from fastapi import HTTPException, status, APIRouter
from data.blog_entries import posts

# -------------------------------- API Routes --------------------------------

router = APIRouter()


@router.get("/api/posts")
def get_posts(title: str | None = None):
    if title:
        for post in posts:
            if post.get("title") == title:
                return post
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No post found with title: {title}.",
        )
    return posts


# Add Query Parameter
@router.get("/api/posts/{post_id}")
def get_post(post_id: int):
    for post in posts:
        # get returns None if key doesnt exist
        # ["id"] return error is key doesnt exist
        if post.get("id") == post_id:
            return post

    # Custome exception
    # raise PostNotFoundError(f"Post {post_id} not found")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    """
    Accept JSON with title, content
    Automatically generate id
    Append to posts
    Return created post
    Return 400 if title is missing
    """


@router.post("/api/create_post")
def create_post(new_post: dict):

    test = [post["id"] for post in posts]
    test.sort()
    new_post["id"] = test[-1] + 1
    posts.append(new_post)
    if new_post.get("title") == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Post title is missing"
        )
    return new_post


""" Remove post if exists
Return 204 on success
Raise 404 if not found """


@router.delete("/api/delete_post/{post_id}")
def delete_post(post_id: int):
    global posts
    ids = [p.get("id") for p in posts]
    if post_id not in ids:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post {post_id} not found"
        )
    else:
        posts = [p for p in posts if p.get("id") != post_id]

    return status.HTTP_204_NO_CONTENT
