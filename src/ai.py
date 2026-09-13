import os

import httpx2


GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-20b"


async def analyze_incident(
    title: str,
    description: str,
    api_key: str | None = None,
) -> str:
    api_key = api_key or os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY não configurada.")

    prompt = f"""
Você é um analista especialista em gestão de incidentes de TI.

Analise o incidente abaixo e forneça uma análise objetiva.

Título:
{title}

Descrição:
{description}

Retorne:
1. Categoria provável
2. Prioridade recomendada
3. Causa provável
4. Recomendação de ação
5. Riscos ou impactos possíveis

Não invente informações que não estejam disponíveis.
Se alguma informação não puder ser determinada, deixe isso explícito.
"""

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Você é um especialista em operações e incidentes de TI.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        "temperature": 0.2,
        "max_tokens": 700,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    async with httpx2.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            GROQ_API_URL,
            headers=headers,
            json=payload,
        )

    response.raise_for_status()

    data = response.json()

    return data["choices"][0]["message"]["content"]
