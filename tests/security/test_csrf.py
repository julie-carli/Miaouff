"""Security tests for CSRF protection."""

import re


def test_post_without_token_is_rejected(csrf_client):
    response = csrf_client.post(
        "/login", data={"action": "login", "email": "a@a.fr", "password": "x"}
    )
    assert response.status_code == 400


def test_post_with_form_token_is_accepted(csrf_client):
    # Fetch a real token from the rendered login form, then reuse it.
    html = csrf_client.get("/login").get_data(as_text=True)
    match = re.search(r'name="csrf_token"[^>]*value="([^"]+)"', html)
    assert match, "csrf_token field should be present in the form"
    token = match.group(1)

    response = csrf_client.post(
        "/login",
        data={
            "action": "login",
            "email": "a@a.fr",
            "password": "x",
            "csrf_token": token,
        },
    )
    assert response.status_code != 400


def test_post_with_header_token_is_accepted(csrf_client):
    html = csrf_client.get("/login").get_data(as_text=True)
    token = re.search(r'name="csrf-token" content="([^"]+)"', html).group(1)

    response = csrf_client.post(
        "/login",
        data={"action": "login", "email": "a@a.fr", "password": "x"},
        headers={"X-CSRFToken": token},
    )
    assert response.status_code != 400
