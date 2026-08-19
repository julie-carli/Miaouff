"""Integration tests for access control on protected routes.

These verify the fix for the previously unprotected admin routes: an anonymous
visitor must never reach an admin or account page, but be redirected to login.
"""

import pytest

ADMIN_ROUTES = [
    "/edit-users",
    "/edit-user/1",
    "/edit_products",
    "/edit-shelters",
    "/edit_animals",
    "/edit_pets",
    "/edit_categories",
    "/edit-articles",
]

LOGIN_REQUIRED_ROUTES = [
    "/account",
    "/edit_profile",
    "/check_order",
    "/delete_account",
]


@pytest.mark.parametrize("route", ADMIN_ROUTES)
def test_admin_routes_block_anonymous(client, route):
    """Anonymous users are redirected (not served the admin page)."""
    response = client.get(route)
    assert response.status_code == 302
    assert "/login" in response.headers.get("Location", "")


@pytest.mark.parametrize("route", LOGIN_REQUIRED_ROUTES)
def test_login_required_routes_redirect_anonymous(client, route):
    response = client.get(route)
    assert response.status_code == 302
    assert "/login" in response.headers.get("Location", "")


def test_delete_user_rejects_anonymous(client):
    """The destructive delete-user endpoint must not be callable anonymously."""
    response = client.post("/delete_user/1")
    assert response.status_code == 302
    assert "/login" in response.headers.get("Location", "")


def test_delete_account_rejects_anonymous(client):
    """Closing an account must require a logged-in session."""
    response = client.post("/delete_account", data={"confirm": "1", "password": "x"})
    assert response.status_code == 302
    assert "/login" in response.headers.get("Location", "")
