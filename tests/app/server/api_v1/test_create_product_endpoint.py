import json


def test_create_product_endpoint(test_app):
    """
    Test to verify that the create product endpoint is working.
    """

    test_request_payload = {
        "title": "Handmade Steel Computer",
        "description": "The Handmade Steel Computer is a great product.",
        "image": "https://example.com/product_image.jpg",
        "price": 1000,
        "currency": "USD",
        "discount": False,
    }

    test_response_payload = {
        "product_id": 1,
        "message": "Product created successfully",
        "title": "Handmade Steel Computer",
        "description": "The Handmade Steel Computer is a great product.",
        "image": "https://example.com/product_image.jpg",
        "price": 1000,
        "currency": "USD",
        "discount": False,
    }

    response = test_app.post(
        "api/v1/products/create",
        content=json.dumps(test_request_payload),
    )

    assert response.status_code == 201
    assert response.json() == test_response_payload
