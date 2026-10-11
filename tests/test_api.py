from fastapi.testclient import TestClient
from backend.api import app



client = TestClient(app)


#tests:
def test_invalid_status():
    response = client.get("/tasks?status_filter=banana")
    assert response.status_code == 422


def test_get_tasks():
    responce = client.get("/tasks")
    assert responce.status_code == 200


