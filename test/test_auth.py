def test_register_and_autologin(client):
    response = client.post("/api/auth/register", json={"email": "wanasit.wt@gmail.com", "password": "abc"})
    assert response.status_code == 200
    assert response.json['email'] == "wanasit.wt@gmail.com"

    response = client.get("/api/auth/status")
    assert response.status_code == 200
    assert response.json['loggedIn'] == True
    assert response.json['email'] == "wanasit.wt@gmail.com"

def test_register_not_autologin(client):
    response = client.post("/api/auth/register?autologin=false", json={"email": "wanasit.wt@gmail.com", "password": "abc"})
    assert response.status_code == 200
    assert response.json['email'] == "wanasit.wt@gmail.com"

    response = client.get("/api/auth/status")
    assert response.status_code == 200
    assert response.json['loggedIn'] == False


def test_duplicate_register(client):
    response = client.post("/api/auth/register", json={"email": "wanasit.wt@gmail.com", "password": "abc"})
    assert response.status_code == 200

    response = client.post("/api/auth/register", json={"email": "wanasit.wt@gmail.com", "password": "abc"})
    assert response.status_code == 400
    assert response.json['message'] == 'Invalid email or password'


def test_login_success(client):
    response = client.get("/api/auth/status")
    assert response.status_code == 200
    assert response.json['loggedIn'] == False

    response = client.post("/api/auth/register?autologin=false", json={"email": "wanasit.wt@gmail.com", "password": "abc"})
    assert response.status_code == 200

    response = client.post("/api/auth/login", json={"email": "wanasit.wt@gmail.com", "password": "abc"})
    assert response.status_code == 200
    assert response.json['email'] == "wanasit.wt@gmail.com"

    response = client.get("/api/auth/status")
    assert response.status_code == 200
    assert response.json['loggedIn'] == True
    assert response.json['email'] == "wanasit.wt@gmail.com"


def test_login_fail(client):
    response = client.get("/api/auth/status")
    assert response.status_code == 200
    assert response.json['loggedIn'] == False

    response = client.post("/api/auth/register?autologin=false", json={"email": "wanasit.wt@gmail.com", "password": "abc"})
    assert response.status_code == 200

    response = client.post("/api/auth/login", json={"email": "wanasit.wt@gmail.com", "password": "xyz"})
    assert response.status_code == 401
    assert response.json['message'] == "Incorrect email or password"

    response = client.get("/api/auth/status")
    assert response.status_code == 200
    assert response.json['loggedIn'] == False


def test_logout(client):
    response = client.get("/api/auth/logout")
    assert response.status_code == 200
    assert response.json['loggedIn'] == False

    response = client.post("/api/auth/register", json={"email": "wanasit.wt@gmail.com", "password": "abc"})
    assert response.status_code == 200
    assert response.json['email'] == "wanasit.wt@gmail.com"

    response = client.get("/api/auth/logout")
    assert response.status_code == 200
    assert response.json['loggedIn'] == True
    assert response.json['email'] == "wanasit.wt@gmail.com"

    response = client.get("/api/auth/status")
    assert response.status_code == 200
    assert response.json['loggedIn'] == False
