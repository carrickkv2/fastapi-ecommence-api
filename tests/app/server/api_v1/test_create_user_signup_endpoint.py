import json

from app.db import operations


def test_create_new_user_endpoint(test_app):
    """
    Test to verify that the create new user endpoint is working.
    """
    test_request_payload = {
        "email": "test@gmail.com",
        "phone_number": "+254-5941025",
        "first_name": "Larry",
        "last_name": "Moe",
        "password": "test_password",
        "password_confirmation": "test_password",
    }

    response = test_app.post(
        "api/v1/auth/signup",
        content=json.dumps(test_request_payload),
    )

    response_json = response.json()
    assert response.status_code == 201
    assert response_json["message"] == "Created a new user successfully"
    assert response_json["email"] == "test@gmail.com"
    assert response_json["phone_number"] == "+254-5941025"
    assert response_json["first_name"] == "Larry"
    assert response_json["last_name"] == "Moe"
    assert "user_id" in response_json


def test_create_new_user_endpoint_returns_relevant_errors(test_app):
    """
    Test to verify that the create new user
    endpoint is working returns the right errors.
    """
    test_request_payload = {
        "email": "test1@gmail.com",
        "phone_number": "+254-5941025",
        "first_name": "Larry",
        "last_name": "Moe",
        "password": "test_password",
        "password_confirmation": "test_password",
    }

    test_app.post(
        "api/v1/auth/signup",
        content=json.dumps(test_request_payload),
    )

    response = test_app.post(
        "api/v1/auth/signup",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "A user with this email address already exists."}
