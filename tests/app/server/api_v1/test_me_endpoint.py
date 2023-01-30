def test_me_endpoint(test_app):
    """
    Test to verify that the me endpoint is working.
    """

    response = test_app.get("api/v1/auth/me")
    assert response.status_code == 200
