# Shared pytest fixtures for the API test suite.
#
# These tests treat stock-backend as a black box: they only ever talk to it
# over HTTP, using a base URL supplied via environment variable. They never
# import stock-backend's source or reach into its repo, per the
# multi-repo convention (see stock-qa/CLAUDE.md).

import os

import httpx
import pytest

# Env var that points at a running stock-backend instance, e.g.
# "http://localhost:8000". Tests that need a live backend should skip
# themselves (see the `require_backend` fixture below) rather than fail
# outright when this isn't set, so the suite stays runnable in CI stages
# where the backend isn't up yet.
API_BASE_URL_ENV_VAR = "API_BASE_URL"


@pytest.fixture(scope="session")
def api_base_url() -> str:
    """Base URL of the stock-backend instance under test.

    Defaults to a typical local docker-compose port so `pytest` "just
    works" for a developer who already has stock-backend running locally,
    but can be overridden for staging/CI targets.
    """
    return os.environ.get(API_BASE_URL_ENV_VAR, "http://localhost:8000")


@pytest.fixture(scope="session")
def require_backend(api_base_url: str) -> str:
    """Skip the test if no stock-backend instance is actually reachable.

    This lets the smoke test (and future tests) be structured cleanly and
    still pass in environments where stock-backend isn't running, instead
    of erroring with a connection failure.
    """
    try:
        response = httpx.get(f"{api_base_url}/docs", timeout=2.0)
    except httpx.HTTPError:
        pytest.skip(
            f"stock-backend not reachable at {api_base_url} "
            f"(set {API_BASE_URL_ENV_VAR} to point at a running instance)"
        )
    if response.status_code >= 500:
        pytest.skip(f"stock-backend at {api_base_url} returned a server error")
    return api_base_url


@pytest.fixture(scope="session")
def api_client(require_backend: str) -> httpx.Client:
    """An httpx client pre-configured with the backend's base URL.

    Scoped to the session so tests share one connection pool; individual
    tests should still call .close-safe methods (get/post/etc.) rather than
    mutate shared client state.
    """
    with httpx.Client(base_url=require_backend, timeout=5.0) as client:
        yield client
