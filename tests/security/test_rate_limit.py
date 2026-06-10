"""Security test for brute-force rate limiting on the login endpoint."""


def test_login_is_rate_limited(ratelimited_client):
    """After the per-minute limit, further login attempts return 429."""
    codes = [
        ratelimited_client.post(
            "/login", data={"action": "login", "email": "a@a.fr", "password": "x"}
        ).status_code
        for _ in range(12)
    ]
    assert 429 in codes
