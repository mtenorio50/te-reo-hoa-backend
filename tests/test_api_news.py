import pytest
from datetime import datetime


@pytest.fixture(autouse=True)
def mock_get_positive_news_from_gemini(monkeypatch):
    async def fake(*args, **kwargs):
        return [{
            "title": "Test News",
            "title_maori": "Panui Whakamatautau",
            "content": "A great thing happened.",
            "summary_maori": "He mea rawe i puta.",
            "link": "https://example.com/test-news-mock",
            "image_url": [],
        }]
    # Patch both the import path and the module path
    monkeypatch.setattr(
        "app.ai_integration.get_positive_news_from_gemini", fake)
    monkeypatch.setattr("app.router.news.get_positive_news_from_gemini", fake)


def test_admin_can_list_all_news(client, register_and_login_admin, db_session):
    # Add a news item to the DB for the test
    from app.models import NewsItem
    news = NewsItem(
        title_english="Test News",
        title_maori="Panui Whakamatautau",
        summary_english="A great thing happened.",
        summary_maori="He mea rawe i puta.",
        published_date=datetime(2023, 6, 30, 0, 0, 0),
        source_url="https://example.com/news1",
        source="UnitTest",
        image_urls=[],
    )
    db_session.add(news)
    db_session.commit()

    token = register_and_login_admin
    resp = client.get(
        "/news/all", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(item["title_english"] == "Test News" for item in data)


def test_learner_cannot_list_all_news(client, register_and_login_learner):
    token = register_and_login_learner
    resp = client.get(
        "/news/all", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403


def test_unauth_cannot_list_all_news(client):
    resp = client.get("/news/all")
    assert resp.status_code == 401


def test_get_latest_news_public(client, db_session):
    # Add news item to DB
    from app.models import NewsItem
    news = NewsItem(
        title_english="Latest News",
        title_maori="Panui Hou",
        summary_english="Another thing happened.",
        summary_maori="He mea anō i puta.",
        published_date=datetime(2023, 7, 1, 0, 0, 0),
        source_url="https://example.com/news2",
        source="UnitTest",
        image_urls=[],
    )
    db_session.add(news)
    db_session.commit()
    resp = client.get("/news/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(item["title_english"] == "Latest News" for item in data)


def test_admin_can_refresh_news(client, register_and_login_admin):
    token = register_and_login_admin
    resp = client.post(
        "/news/refresh", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    data = resp.json()
    assert "added" in data
    assert "message" in data
    # The mock returns 1 item, but the actual function may return more based on the AI response
    assert data["added"] >= 1


def test_learner_cannot_refresh_news(client, register_and_login_learner):
    token = register_and_login_learner
    resp = client.post(
        "/news/refresh", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403


def test_unauth_cannot_refresh_news(client):
    resp = client.post("/news/refresh")
    assert resp.status_code == 401


def test_admin_can_delete_news(client, register_and_login_admin, db_session):
    from app.models import NewsItem
    # Add news item to DB
    news = NewsItem(
        title_english="To Delete",
        title_maori="Mukua",
        summary_english="Delete me.",
        summary_maori="Mukua ahau.",
        published_date=datetime(2023, 7, 1, 0, 0, 0),
        source_url="https://example.com/newsdelete",
        source="UnitTest",
        image_urls=[],
    )
    db_session.add(news)
    db_session.commit()
    news_id = news.id
    token = register_and_login_admin
    resp = client.delete(f"/news/{news_id}",
                         headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200


def test_delete_nonexistent_news_returns_404(client, register_and_login_admin):
    token = register_and_login_admin
    resp = client.delete(
        f"/news/999999", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 404
