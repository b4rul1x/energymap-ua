from fastapi.testclient import TestClient

from backend.app import main
from backend.app.integrations.svitlopulse import OblastStatus, SourceError

client = TestClient(main.app)


def make_region(**overrides):
    data = {
        "slug": "test-oblast",
        "iso": "UA-00",
        "name_uk": "Тестова область",
        "state": "partial",
        "stale": False,
    }
    data.update(overrides)
    return OblastStatus(**data)


def test_has_data_true_for_fresh_known_state():
    assert make_region().has_data is True


def test_has_data_false_for_unknown_and_stale():
    region = make_region(state="unknown", stale=True)
    assert region.has_data is False


def test_map_status_returns_503_when_source_fails(monkeypatch):
    async def broken_source():
        raise SourceError("тест: джерело впало")

    monkeypatch.setattr(main, "fetch_oblasts", broken_source)

    response = client.get("/api/v1/map/status")

    assert response.status_code == 503