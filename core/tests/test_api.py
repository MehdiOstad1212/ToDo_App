def test_login_response_401(anon_client):
    payload = {"user_name": "eli",
               "password": "1248"}
    response = anon_client.post("/users/login", json = payload)
    assert response.status_code == 401

def test_register_response_201 (anon_client):
    payload = {"user_name": "eli",
                "password": "1212",
                "password_confirm": "1212"
                        }
    response = anon_client.post("/users/register", json = payload)
    assert response.status_code == 201