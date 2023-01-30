import json


def test_update_order(test_app):
    """
    Test to verify that a user can update their order.
    """

    test_signup_request_payload = {
        "email": "test@gmail.com",
        "phone_number": "+254-5941025",
        "first_name": "Larry",
        "last_name": "Moe",
        "password": "test_password",
        "password_confirmation": "test_password",
    }

    test_app.post(
        "api/v1/auth/signup",
        content=json.dumps(test_signup_request_payload),
    )

    test_product_request_payload = {
        "title": "Handmade Steel Computer",
        "description": "The Handmade Steel Computer is a great product.",
        "image": "https://example.com/product_image.jpg",
        "price": 1000,
        "currency": "USD",
        "discount": False,
    }

    for i in range(3):
        test_product_request_payload["title"] += str(i)
        test_app.post(
            "api/v1/products/create",
            content=json.dumps(test_product_request_payload),
        )

    test_order_request_payload = {
        "email": "test@gmail.com",
        "phone_number": "+254-5941025",
        "products": [
            {"product_name": "Test product 1", "product_id": 1, "quantity": 3},
            {"product_name": "Test product 2", "product_id": 2, "quantity": 2},
        ],
    }

    test_app.post(
        "api/v1/orders/create",
        content=json.dumps(test_order_request_payload),
    )

    test_request_payload = {
        "email": "test@gmail.com",
        "phone_number": "+254-5941025",
        "products": [
            {"product_id": 1, "quantity": 7},
            {"product_id": 2, "quantity": 5},
        ],
    }

    response = test_app.post(
        "api/v1/orders/update/1",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
