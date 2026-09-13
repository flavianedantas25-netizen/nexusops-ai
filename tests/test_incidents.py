from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_create_incident():
    payload = {
        "title": "Sistema ERP indisponível",
        "description": "Todos os usuários estão sem acesso ao sistema ERP.",
        "requester": "Flaviane",
        "area": "Financeiro",
        "category": "Sistemas",
        "impact_users": 50,
        "urgency": "alta",
    }

    response = client.post(
        "/api/v1/incidents",
        json=payload,
    )

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["requester"] == payload["requester"]
    assert data["area"] == payload["area"]
    assert data["impact_users"] == payload["impact_users"]
    assert data["urgency"] == payload["urgency"]

    assert data["status"] == "aberto"
    assert data["priority"] in {"baixa", "media", "alta", "critica"}

    assert data["ai_category"] is not None
    assert data["ai_priority"] is not None
    assert data["ai_confidence"] is not None


def test_list_incidents():
    response = client.get("/api/v1/incidents")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
    assert len(data) > 0


def test_get_incident():
    payload = {
        "title": "Teste de consulta de incidente",
        "description": "Incidente criado para validar a consulta por ID.",
        "requester": "Flaviane",
        "area": "TI",
        "category": "Sistemas",
        "impact_users": 10,
        "urgency": "media",
    }

    create_response = client.post(
        "/api/v1/incidents",
        json=payload,
    )

    assert create_response.status_code == 201

    created_incident = create_response.json()
    incident_id = created_incident["id"]

    response = client.get(
        f"/api/v1/incidents/{incident_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == incident_id
    assert data["title"] == payload["title"]
    assert data["requester"] == payload["requester"]
    assert data["ai_category"] is not None
    assert data["ai_priority"] is not None
    assert data["ai_confidence"] is not None
