def test_login_invalid_data_response_401(anon_client):
    payload = {"user_name": "eli",
               "password": "1248"}
    response = anon_client.post("/users/login", json = payload)
    assert response.status_code == 401

    payload = {"user_name": "usertest",
                   "password": "1248"}
    response = anon_client.post("/users/login", json = payload)
    assert response.status_code == 401

def test_login_response_200(anon_client):
    payload = {"user_name": "usertest",
               "password": "12345678910"}
    response = anon_client.post("/users/login", json = payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_register_response_201 (anon_client):
    payload = {"user_name": "eli",
                "password": "1212",
                "password_confirm": "1212"
                        }
    response = anon_client.post("/users/register", json = payload)
    assert response.status_code == 201