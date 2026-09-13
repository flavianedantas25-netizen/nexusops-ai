from backend.app.services.classifier import classify_incident, classify_priority


def test_classify_incident_erp():
    category, confidence = classify_incident(
        "Sistema ERP indisponível",
        "Usuários não conseguem acessar o sistema ERP."
    )

    assert category == "Sistemas"
    assert confidence >= 0.80


def test_classify_priority_critical():
    priority, confidence = classify_priority(
        50,
        "alta",
        "Sistema ERP indisponível",
        "Todos os usuários estão sem acesso."
    )

    assert priority == "critica"
    assert confidence >= 0.90
