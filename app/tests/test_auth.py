def test_register_user_success(client):
    response = client.post(
        "/auth/register",
        json={"username": "newuser", "email": "new@example.com", "password": "securepass"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert "password" not in data  # la contraseña nunca debe devolverse

def test_register_user_duplicate(client):
    client.post("/auth/register", json={"username": "dupeuser", "email": "dupe@example.com", "password": "pass123"})
    response = client.post("/auth/register", json={"username": "dupeuser", "email": "dupe@example.com", "password": "pass123"})
    assert response.status_code == 400

def test_login_success(client):
    client.post("/auth/register", json={"username": "loginuser", "email": "login@example.com", "password": "pass123"})
    response = client.post("/auth/login", json={"username_or_email": "loginuser", "password": "pass123"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "loginuser"
    assert "id" in data

def test_login_with_email(client):
    client.post("/auth/register", json={"username": "emailuser", "email": "email@example.com", "password": "pass123"})
    response = client.post("/auth/login", json={"username_or_email": "email@example.com", "password": "pass123"})
    assert response.status_code == 200

def test_login_incorrect_password(client):
    client.post("/auth/register", json={"username": "wrongpass", "email": "wrong@example.com", "password": "correct"})
    response = client.post("/auth/login", json={"username_or_email": "wrongpass", "password": "incorrect"})
    assert response.status_code == 401
