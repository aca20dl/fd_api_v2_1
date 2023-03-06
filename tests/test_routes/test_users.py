import json


def test_create_user(client):
    data = {"company_name":"testcompany","email":"testcompany@nofoobar.com",
            "password":"testing", "company_id":"111111",
            "company_category":"grocery_pos"}
    response = client.post("/", json.dumps(data))
    assert response.status_code == 200
    assert response.json()["email"] == "testcompany@nofoobar.com"
    assert response.json()["company_name"] == "testcompany"