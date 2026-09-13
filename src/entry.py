from fastapi import FastAPI, HTTPException, Request

from schemas.incident import (
    IncidentAIAnalysisRequest,
    IncidentAIAnalysisResponse,
)
from ai import analyze_incident
from workers import asgi


app = FastAPI(
    title="NexusOps AI",
    description="Plataforma inteligente para gestão, triagem e análise de incidentes corporativos.",
    version="0.2.0",
)


@app.get("/")
async def root():
    return {
        "name": "NexusOps AI",
        "status": "online",
        "version": "0.2.0",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post(
    "/api/v1/incidents/analyze",
    response_model=IncidentAIAnalysisResponse,
)
async def analyze_incident_with_ai(
    incident_data: IncidentAIAnalysisRequest,
    request: Request,
):
    try:
        env = request.scope["env"]
        api_key = env.GROQ_API_KEY

        analysis = await analyze_incident(
            incident_data.title,
            incident_data.description,
            api_key=api_key,
        )

        return IncidentAIAnalysisResponse(
            title=incident_data.title,
            description=incident_data.description,
            analysis=analysis,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Não foi possível realizar a análise com IA: {exc}",
        )


Default = asgi.entrypoint(app)
