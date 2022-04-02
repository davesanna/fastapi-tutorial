def test_vote_on_post(authorized_client, test_posts, test_user2):

    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[0].id, "direction": 1}
    )
    assert res.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):

    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "direction": 1}
    )
    assert res.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):

    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "direction": 0}
    )
    assert res.status_code == 201


def test_delete_vote_non_exist(authorized_client, test_posts):

    res = authorized_client.post(
        "/vote/", json={"post_id": test_posts[3].id, "direction": 0}
    )
    assert res.status_code == 404


def test_vote_post_non_exist(authorized_client, test_posts):

    res = authorized_client.post("/vote/", json={"post_id": 2341241, "direction": 1})
    assert res.status_code == 404


def test_vote_unathorized_user(client, test_posts):

    res = client.post("/vote/", json={"post_id": test_posts[3].id, "direction": 1})
    assert res.status_code == 401
