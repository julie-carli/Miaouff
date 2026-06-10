"""Integration tests for public pages that do not hit the database."""

import pytest

PUBLIC_ROUTES = [
    "/",
    "/contact",
    "/faq",
    "/privacy_policy",
    "/cookie_policy",
    "/legal_notices",
    "/terms_conditions",
    "/animals",
    "/games",
    "/quiz",
    "/match",
    "/memory",
    "/wordsearch",
    "/hangman",
    "/rapido",
]


@pytest.mark.parametrize("route", PUBLIC_ROUTES)
def test_public_route_returns_200(client, route):
    assert client.get(route).status_code == 200


def test_security_headers_present(client):
    headers = client.get("/").headers
    assert headers.get("X-Content-Type-Options") == "nosniff"
    assert headers.get("X-Frame-Options") == "SAMEORIGIN"
    assert "Content-Security-Policy" in headers
    assert "Strict-Transport-Security" in headers


def test_cookie_banner_is_rendered(client):
    html = client.get("/").get_data(as_text=True)
    assert 'id="cookie-banner"' in html
    assert "Refuser tout" in html
    assert "Accepter tout" in html


def test_unknown_page_returns_404(client):
    assert client.get("/this-page-does-not-exist").status_code == 404
