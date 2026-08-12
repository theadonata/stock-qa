# Smoke test: the bare minimum check that a stock-backend instance is up
# and serving its API. This is intentionally shallow — it is not testing
# business logic (COGS, stock ledger, P&L), just that the deployed
# service responds. Deeper endpoint tests belong in their own test files.
#
# Per stock-qa's scope, this suite targets stock-backend's *deployed* HTTP
# surface (its OpenAPI docs page at /docs, per the design spec), never its
# source tree.

import pytest


@pytest.mark.smoke
def test_backend_docs_endpoint_is_reachable(api_client):
    """The FastAPI auto-generated /docs page should load with a 2xx status.

    This is the cheapest possible signal that stock-backend is deployed,
    running, and serving requests at all — a prerequisite for every other
    test in this suite. If this fails, every other API test would fail for
    the same underlying reason (backend not up), so it's useful to see this
    fail first and distinctly.
    """
    response = api_client.get("/docs")
    assert response.status_code == 200


@pytest.mark.smoke
def test_backend_openapi_schema_is_served(api_client):
    """FastAPI exposes a machine-readable OpenAPI schema at /openapi.json.

    Checking this (rather than just /docs) confirms the app actually wired
    up its routes, not just that some HTTP server is listening on the port.
    """
    response = api_client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    # A minimal sanity check that this is really an OpenAPI document.
    assert "openapi" in schema
    assert "paths" in schema
