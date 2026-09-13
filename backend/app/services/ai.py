import os

from dotenv import load_dotenv
from groq import Groq


load_dotenv()


def analyze_incident(title: str, description: str) -> str:
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY não configurada.")

    client = Groq(api_key=api_key)

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

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": "Você é um especialista em operações e incidentes de TI.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.2,
        max_tokens=700,
    )

    return response.choices[0].message.content
