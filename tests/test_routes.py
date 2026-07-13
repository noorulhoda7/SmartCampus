from app import create_app


def test_public_pages_load():
    app = create_app()
    client = app.test_client()

    assert client.get("/").status_code == 200
    assert client.get("/view_attendance").status_code == 200


def test_invalid_login_is_rejected():
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/login",
        data={"username": "invalid", "password": "invalid", "role": "Student"},
    )

    assert response.status_code == 200
    assert response.data == b"Invalid credentials"


def test_admin_login_redirects_to_dashboard():
    app = create_app()
    client = app.test_client()

    response = client.post(
        "/login",
        data={"username": "admin", "password": "admin", "role": "admin"},
        follow_redirects=False,
    )

    assert response.status_code == 302
    assert response.headers["Location"].endswith("/admin")
