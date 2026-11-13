"""Exercise request policy and its registration on the real Studio app."""

import pytest
from fastapi.testclient import TestClient

from server import workbench
from server.main import app


@pytest.fixture
def studio(tmp_path, monkeypatch):
    workbench.close_workbench()
    monkeypatch.setenv("PROMPT_STUDIO_DATA", str(tmp_path / "workspace"))
    with TestClient(app, base_url="http://127.0.0.1:8000") as client:
        yield client


def test_local_form_policy_and_posts(studio):
    page = studio.get("/")
    assert page.headers["referrer-policy"] == "same-origin"
    assert page.headers["x-frame-options"] == "DENY"
    assert page.headers["x-content-type-options"] == "nosniff"
    assert page.headers["cache-control"] == "no-store"
    response = studio.post("/studio/example", headers={
        "Origin": "http://127.0.0.1:8000", "Sec-Fetch-Site": "same-origin",
    }, follow_redirects=False)
    assert response.status_code == 303
    assert len(workbench.get_store().runs()) == 1


def test_originless_local_cli_works(studio):
    assert studio.post("/studio/example", follow_redirects=False).status_code == 303


@pytest.mark.parametrize("headers", [
    {"Origin": "null", "Sec-Fetch-Site": "same-origin"},
    {"Origin": "https://other.example", "Sec-Fetch-Site": "same-site"},
    {"Origin": "http://127.0.0.1:9999", "Sec-Fetch-Site": "same-origin"},
    {"Origin": "http://127.0.0.1:8000", "Sec-Fetch-Site": "cross-site"},
    {"Origin": "http://[invalid", "Sec-Fetch-Site": "same-origin"},
    {"Origin": "http://127.0.0.1:8000/unexpected-path"},
    {"Sec-Fetch-Site": "same-site"},
])
def test_untrusted_mutations_are_rejected_before_saving(studio, headers):
    response = studio.post("/studio/example", headers=headers)
    assert response.status_code == 403
    assert response.text == "Open this action from your local Studio tab."
    assert workbench.get_store().runs() == []


def test_foreign_host_cannot_mutate(studio):
    response = studio.post("/studio/example", headers={"Host": "foreign.example"})
    assert response.status_code == 400
    assert workbench.get_store().runs() == []


def test_validation_omits_private_input_and_schema_stays_local(studio):
    response = studio.post("/meta-chain/design", json={"goal": {"private-fixture": "confidential-value"}})
    assert response.status_code == 422
    assert "private-fixture" not in response.text
    assert "confidential-value" not in response.text
    assert studio.get("/docs").status_code == 404
    assert studio.get("/openapi.json").status_code == 200
