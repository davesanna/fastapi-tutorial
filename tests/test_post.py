def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)
