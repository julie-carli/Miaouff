"""Unit tests for the file-upload extension whitelist (no database needed)."""

import pytest

from services.shelter_service import allowed_file


@pytest.mark.parametrize(
    "filename",
    ["photo.png", "photo.jpg", "photo.jpeg", "photo.gif", "PHOTO.PNG", "a.b.jpg"],
)
def test_allowed_extensions(filename):
    assert allowed_file(filename) is True


@pytest.mark.parametrize(
    "filename",
    ["script.php", "archive.zip", "doc.pdf", "noextension", "evil.exe", ".gitignore"],
)
def test_rejected_extensions(filename):
    assert allowed_file(filename) is False
