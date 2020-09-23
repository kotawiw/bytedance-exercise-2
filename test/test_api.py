import pytest
import time


@pytest.fixture
def logged_in_user(client):
    user = {"email": "some_email@gmail.com", "password": "abc"}
    response = client.post("/api/auth/register?autologin=true", json=user)
    assert response.status_code == 200
    assert response.json['email'] == user["email"]
    return logged_in_user



def test_create_event(client, logged_in_user):
    response = client.post("/api/events", json={
        "name": "abc",
        "location": "Tokyo",
        "startTimestamp": int(time.time() * 1000),
        "endTimestamp": int((time.time() + + 3600) * 1000)
    })

    assert response.status_code == 200, response.json
    assert response.json['name'] == 'abc', response.json
    assert response.json['location'] == 'Tokyo', response.json


def test_create_event_not_login(client):
    response = client.post("/api/events", json={
        "name": "abc",
        "location": "Tokyo",
        "startTimestamp": int(time.time() * 1000),
        "endTimestamp": int((time.time() + + 3600) * 1000)
    })

    assert response.status_code == 401, response.json


def test_query(client, logged_in_user):
    ref_timestamp = int(time.time() * 1000)

    client.post("/api/events", json={
        "name": "Event1",
        "location": "Tokyo",
        "startTimestamp": ref_timestamp + 100,
        "endTimestamp": ref_timestamp + 100 + 3600_000
    })

    client.post("/api/events", json={
        "name": "Event2",
        "location": "Tokyo",
        "startTimestamp": ref_timestamp,
        "endTimestamp": ref_timestamp + 3600_000
    })

    response = client.get("/api/events")

    assert response.status_code == 200, response.json
    assert response.json['totalCount'] == 2
    assert response.json['values'][0]['name'] == 'Event2'
    assert response.json['values'][1]['name'] == 'Event1'


def test_event_registration(client, logged_in_user):
        ref_timestamp = int(time.time() * 1000)

        event = client.post("/api/events", json={
            "name": "Event1",
            "location": "Tokyo",
            "startTimestamp": ref_timestamp + 100,
            "endTimestamp": ref_timestamp + 100 + 3600_000
        }).json

        assert event['id'], event

        response = client.get("/api/event/%s/registrations" % event['id'])
        assert response.status_code == 200, response.json
        assert len(response.json) == 0

        _register_and_login(client, 'user1@gmail.com')
        response = client.put("/api/event/%s/registrations" % event['id'])
        assert response.status_code == 200, response.json

        _register_and_login(client, 'user2@gmail.com')
        response = client.put("/api/event/%s/registrations" % event['id'])
        assert response.status_code == 200, response.json

        response = client.get("/api/event/%s/registrations" % event['id'])
        assert response.status_code == 200, response.json
        assert len(response.json) == 2
        assert response.json[0]['email'] == 'user1@gmail.com'
        assert response.json[1]['email'] == 'user2@gmail.com'

        _login(client, 'user1@gmail.com')
        response = client.delete("/api/event/%s/registrations" % event['id'])
        assert response.status_code == 200, response.json

        response = client.get("/api/event/%s/registrations" % event['id'])
        assert response.status_code == 200, response.json
        assert len(response.json) == 1
        assert response.json[0]['email'] == 'user2@gmail.com'



def _login(client, email):
    user = {"email": email, "password": "abc"}
    response = client.post("/api/auth/login", json=user)
    assert response.status_code == 200
    assert response.json['email'] == user["email"]

def _register_and_login(client, email):
    user = {"email": email, "password": "abc"}
    response = client.post("/api/auth/register?autologin=true", json=user)
    assert response.status_code == 200
    assert response.json['email'] == user["email"]

