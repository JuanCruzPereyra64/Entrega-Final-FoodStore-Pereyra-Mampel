from fastapi import status


def test_registro_ok(client):
    res = client.post("/api/v1/auth/registro", json={
        "nombre": "Nuevo", "apellido": "User",
        "email": "nuevo@test.com", "password": "12345678"
    })
    assert res.status_code == status.HTTP_201_CREATED
    data = res.json()
    assert data["email"] == "nuevo@test.com"
    assert "id" in data


def test_registro_email_duplicado(client):
    client.post("/api/v1/auth/registro", json={
        "nombre": "Nuevo", "apellido": "User",
        "email": "dup@test.com", "password": "12345678"
    })
    res = client.post("/api/v1/auth/registro", json={
        "nombre": "Otro", "apellido": "User",
        "email": "dup@test.com", "password": "12345678"
    })
    assert res.status_code == status.HTTP_400_BAD_REQUEST


def test_login_ok(client):
    res = client.post("/api/v1/auth/login", json={
        "email": "client@test.com", "password": "Client1234"
    })
    assert res.status_code == status.HTTP_200_OK
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalido(client):
    res = client.post("/api/v1/auth/login", json={
        "email": "client@test.com", "password": "WrongPass1"
    })
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


def test_logout(client):
    login_res = client.post("/api/v1/auth/login", json={
        "email": "client@test.com", "password": "Client1234"
    })
    assert login_res.status_code == 200
    login_data = login_res.json()
    refresh_token = login_data["refresh_token"]
    access_token = login_data["access_token"]

    res = client.post(
        "/api/v1/auth/logout",
        json=refresh_token,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert res.status_code == status.HTTP_204_NO_CONTENT, res.text


def test_me_authenticated(client, client_headers):
    res = client.get("/api/v1/auth/me", headers=client_headers)
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["email"] == "client@test.com"


def test_me_unauthenticated(client):
    res = client.get("/api/v1/auth/me")
    assert res.status_code == status.HTTP_401_UNAUTHORIZED
