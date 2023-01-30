import json


def test_create_order_endpoint(test_app):
    """
    Test to verify that the create order endpoint is working.
    """

    test_order_request_payload = {
        "email": "test@gmail.com",
        "phone_number": "+254-5941025",
        "products": [
            {"product_name": "Test product 1", "product_id": 1, "quantity": 3},
            {"product_name": "Test product 2", "product_id": 2, "quantity": 2},
        ],
    }

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

    response = test_app.post(
        "api/v1/orders/create",
        content=json.dumps(test_order_request_payload),
    )

    assert response.status_code == 201
    assert response.json()["email"] == "test@gmail.com"
    assert response.json()["phone_number"] == "+254-5941025"
    assert response.json()["products"] == [
        {
            "product_id": 1,
            "quantity": 3,
            "product_title": "Handmade Steel Computer0",
            "product_description": "The Handmade Steel Computer is a great product.",
            "product_image": "https://example.com/product_image.jpg",
            "currency": "USD",
            "product_price": 1000,
        },
        {
            "product_id": 2,
            "quantity": 2,
            "product_title": "Handmade Steel Computer01",
            "product_description": "The Handmade Steel Computer is a great product.",
            "product_image": "https://example.com/product_image.jpg",
            "currency": "USD",
            "product_price": 1000,
        },
    ]
    assert response.json()["order_id"] == 1
    assert response.json()["total_amount"] == 5000
    assert "unique_reference_code" in response.json()
    assert response.json()["status"] == "success"
    assert response.json()["message"] == "Order created successfully"
    assert "date_created" in response.json()
