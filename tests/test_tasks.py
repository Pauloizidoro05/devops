def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_task(client):
    payload = {"title": "Estudar CI/CD", "description": "Ler sobre pipelines", "priority": "high"}
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["priority"] == "high"
    assert data["done"] is False
    assert "id" in data


def test_create_task_invalid_payload(client):
    # título vazio deve ser rejeitado pela validação do Pydantic
    response = client.post("/tasks", json={"title": ""})
    assert response.status_code == 422


def test_list_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_after_creation(client):
    client.post("/tasks", json={"title": "Tarefa 1"})
    client.post("/tasks", json={"title": "Tarefa 2"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_task_by_id(client):
    created = client.post("/tasks", json={"title": "Buscar essa"}).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Buscar essa"


def test_get_task_not_found(client):
    response = client.get("/tasks/9999")
    assert response.status_code == 404


def test_update_task(client):
    created = client.post("/tasks", json={"title": "Original"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"done": True})
    assert response.status_code == 200
    assert response.json()["done"] is True
    assert response.json()["title"] == "Original"


def test_update_task_not_found(client):
    response = client.patch("/tasks/9999", json={"done": True})
    assert response.status_code == 404


def test_delete_task(client):
    created = client.post("/tasks", json={"title": "Apagar"}).json()
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204

    get_response = client.get(f"/tasks/{created['id']}")
    assert get_response.status_code == 404


def test_delete_task_not_found(client):
    response = client.delete("/tasks/9999")
    assert response.status_code == 404
