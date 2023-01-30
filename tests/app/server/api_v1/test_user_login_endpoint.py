import json


def test_login_user_endpoint(test_app):
    """
    Test to verify that the login user endpoint is working.
    """

    test_signup_request_payload = {
        "email": "test@gmail.com",
        "phone_number": "+254-5941025",
        "first_name": "Larry",
        "last_name": "Moe",
        "password": "test_password",
        "password_confirmation": "test_password",
    }

    test_login_request_payload = {"username": "test@gmail.com", "password": "test_password"}

    test_app.post(
        "api/v1/auth/signup",
        content=json.dumps(test_signup_request_payload),
    )

    response = test_app.post("api/v1/auth/login", data=test_login_request_payload)

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"
    assert "message" in response.json()
    assert response.json()["message"] == "Logged in user successfully"
