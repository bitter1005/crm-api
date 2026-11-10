def stages_by_status(response):
    return {s["status"]: s for s in response.data["stages"]}


def test_funnel_for_admin(api, boss, data):
    response = api(boss).get("/api/analytics/funnel/")
    stages = stages_by_status(response)
    assert stages["won"]["count"] == 1
    assert stages["won"]["total"] == 100000
    assert stages["lost"]["count"] == 1
    assert stages["new"]["count"] == 0
    assert response.data["conversion_percent"] == 50


def test_funnel_for_manager_shows_only_own(api, manager_b, data):
    response = api(manager_b).get("/api/analytics/funnel/")
    stages = stages_by_status(response)
    assert stages["lost"]["count"] == 1
    assert stages["won"]["count"] == 0
    assert response.data["conversion_percent"] == 0


def test_revenue_count_only_won_deals(api, boss, data):
    response = api(boss).get("/api/analytics/managers/")
    assert len(response.data) == 1
    assert response.data[0]["owner__username"] == "manager_a"
    assert response.data[0]["revenue"] == 100000
