from typing import Tuple


def classify_incident(title: str, description: str) -> Tuple[str, float]:
    """
    Classifica automaticamente um incidente com base no conteúdo informado.

    Retorna:
        category: categoria prevista pela IA
        confidence: nível de confiança da classificação
    """

    text = f"{title} {description}".lower()

    categories = {
        "Sistemas": [
            "erp",
            "sistema",
            "sistemas",
            "aplicação",
            "aplicativo",
            "software",
            "indisponível",
            "erro no sistema",
            "sistema fora",
        ],
        "Acesso": [
            "login",
            "senha",
            "acesso",
            "acessar",
            "bloqueado",
            "permissão",
            "credencial",
            "usuário",
        ],
        "Infraestrutura": [
            "servidor",
            "rede",
            "vpn",
            "internet",
            "wi-fi",
            "wifi",
            "infraestrutura",
            "computador",
            "notebook",
            "storage",
        ],
        "Financeiro": [
            "financeiro",
            "pagamento",
            "pagamentos",
            "boleto",
            "nota fiscal",
            "nf",
            "fatura",
            "contas a pagar",
            "contas a receber",
        ],
        "Dados": [
            "banco de dados",
            "database",
            "sql",
            "mysql",
            "dados",
            "consulta",
            "relatório",
            "informação",
        ],
        "Integração": [
            "api",
            "integração",
            "webhook",
            "endpoint",
            "integração entre sistemas",
        ],
    }

    scores = {}

    for category, keywords in categories.items():
        score = 0

        for keyword in keywords:
            if keyword in text:
                score += 1

        scores[category] = score

    best_category = max(scores, key=scores.get)
    best_score = scores[best_category]

    if best_score == 0:
        return "Outros", 0.50

    confidence = min(0.95, 0.60 + (best_score * 0.08))

    return best_category, round(confidence, 2)


def classify_priority(
    impact_users: int,
    urgency: str,
    title: str,
    description: str,
) -> Tuple[str, float]:
    """
    Sugere automaticamente a prioridade do incidente.

    A classificação considera:
    - quantidade de usuários afetados;
    - urgência informada;
    - termos críticos encontrados na descrição.

    Retorna:
        priority: prioridade sugerida
        confidence: nível de confiança
    """

    text = f"{title} {description}".lower()
    urgency_normalized = urgency.lower().strip()

    critical_keywords = [
        "indisponível",
        "parado",
        "paralisação",
        "todos os usuários",
        "empresa inteira",
        "produção parada",
        "sistema fora",
        "não funciona",
    ]

    critical_detected = any(
        keyword in text for keyword in critical_keywords
    )

    if impact_users >= 50:
        return "critica", 0.95

    if impact_users >= 20 or urgency_normalized == "alta":
        if critical_detected:
            return "critica", 0.93

        return "alta", 0.90

    if impact_users >= 5 or urgency_normalized == "media":
        return "media", 0.85

    return "baixa", 0.80
