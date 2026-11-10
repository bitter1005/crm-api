from django.utils import timezone

from apps.deals.models import Deal, Task


def test_anonymous_gets_401(api, data):
    assert api().get("/api/deals/").status_code == 401


def test_manager_sees_only_own_deals(api, manager_a, data):
    response = api(manager_a).get("/api/deals/")
    assert response.status_code == 200
    assert {d["id"] for d in response.data["results"]} == {data.deal_a.id}


def test_admin_sees_all_deals(api, boss, data):
    assert api(boss).get("/api/deals/").data["count"] == 2


def test_foreign_deal_returns_404(api, manager_b, data):
    response = api(manager_b).get(f"/api/deals/{data.deal_a.id}/")
    assert response.status_code == 404


def test_manager_cannot_delete_foreign_deal(api, manager_b, data):
    response = api(manager_b).delete(f"/api/deals/{data.deal_a.id}/")
    assert response.status_code == 404
    assert Deal.objects.filter(id=data.deal_a.id).exists()


def test_owner_comes_from_user_not_from_body(api, manager_a, manager_b, data):
    payload = {
        "title": "New",
        "client": data.client_a.id,
        "amount": "10.00",
        "owner": manager_b.id,
    }
    response = api(manager_a).post("/api/deals/", payload, format="json")
    assert response.status_code == 201
    assert response.data["owner"] == manager_a.id


def test_cannot_create_deal_for_foreign_client(api, manager_a, data):
    payload = {"title": "X", "client": data.client_b.id, "amount": "10.00"}
    response = api(manager_a).post("/api/deals/", payload, format="json")
    assert response.status_code == 400
    assert "client" in response.data


def test_cannot_comment_foreign_deal(api, manager_b, data):
    playload = {"deal": data.deal_a.id, "text": "hi"}
    response = api(manager_b).post("/api/comments/", playload, format="json")
    assert response.status_code == 400
    assert "deal" in response.data


def test_comment_author_comes_from_user(api, manager_a, data):
    playload = {"deal": data.deal_a.id, "text": "ok"}
    response = api(manager_a).post("/api/comments/", playload, format="json")
    assert response.status_code == 201
    assert response.data["author"] == manager_a.id


def test_assignee_sees_task_in_foreing_deal(api, manager_b, data):
    Task.objects.create(
        deal=data.deal_a, assignee=manager_b, title="For B", due_date=timezone.now()
    )
    response = api(manager_b).get("/api/tasks/")
    assert {t["title"] for t in response.data["results"]} == {"For B"}
