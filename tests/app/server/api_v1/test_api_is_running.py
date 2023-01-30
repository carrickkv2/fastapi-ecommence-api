def test_that_api_is_working(test_app):
    """
    Test to verify that the API is running.
    """
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "API is running"}
