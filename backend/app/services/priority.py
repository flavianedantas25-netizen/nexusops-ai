def calculate_priority(impact_users: int, urgency: str) -> str:
    """
    Calcula a prioridade do incidente com base no impacto
    e na urgência informados.
    """

    urgency = urgency.lower()

    if impact_users >= 50 and urgency == "alta":
        return "critica"

    if impact_users >= 20 or urgency == "alta":
        return "alta"

    if impact_users >= 5 or urgency == "media":
        return "media"

    return "baixa"
