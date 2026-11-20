def test_schema_is_generated(api):
    response = api().get("/api/schema/")
    assert response.status_code == 200


def test_swagger_ui_is_public(api):
    assert api().get("/api/docs/").status_code == 200