from backend.app.services.priority import calculate_priority


def test_priority_critical():
    result = calculate_priority(50, "alta")
    assert result == "critica"


def test_priority_high():
    result = calculate_priority(20, "alta")
    assert result == "alta"


def test_priority_medium():
    result = calculate_priority(10, "media")
    assert result == "media"


def test_priority_low():
    result = calculate_priority(1, "baixa")
    assert result == "baixa"
