import pytest
from app.schemas.schemas import PostOut, PostResponse


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")

    # validate response with pydantic schema
    def validate(post):
        return PostOut(**post)

    posts_list = list(map(validate, res.json()))

    print(res.json())
    print(posts_list)  # just to check == response

    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)


def test_unathorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_unathorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/8888")
    assert res.status_code == 404


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    print(res.json())

    post = PostOut(**res.json())

    assert post.PostTable.id == test_posts[0].id
    assert post.PostTable.content == test_posts[0].content
    assert post.PostTable.title == test_posts[0].title
    assert res.status_code == 200


@pytest.mark.parametrize(
    "title, content, published",
    [
        ("Awesome title", "test content", True),
        ("Awesome", "test content", False),
        ("tallest skyscraper", "wahoo", True),
    ],
)
def test_create_post(
    authorized_client, test_user, test_posts, title, content, published
):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published}
    )

    created_post = PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.owner_id == test_user["id"]


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    res = authorized_client.post(
        "/posts/", json={"title": "test", "content": "content"}
    )

    created_post = PostResponse(**res.json())

    assert res.status_code == 201
    assert created_post.title == "test"
    assert created_post.content == "content"
    assert created_post.published == True
    assert created_post.owner_id == test_user["id"]


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "test", "content": "content"})

    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(
        f"/posts/{test_posts[0].id}",
    )

    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[0].id}",
    )

    assert res.status_code == 204


def test_delete_post_non_existing(authorized_client, test_user, test_posts):
    res = authorized_client.delete(
        "/posts/342323423",
    )

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_user2, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}",
    )

    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = PostResponse(**res.json())
    assert res.status_code == 200
    assert updated_post.title == "updated title"
    assert updated_post.content == "updated content"


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id,
    }

    res = authorized_client.put(f"/posts/{test_posts[3].id}", json=data)
    assert res.status_code == 403


def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }

    res = client.put(f"/posts/{test_posts[0].id}", json=data)

    assert res.status_code == 401


def test_update_post_non_existing(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id,
    }

    res = authorized_client.put("/posts/342323423", json=data)

    assert res.status_code == 404
