from fastapi import FastAPI, HTTPException, Query, Request

from ai import analyze_incident
from database import (
    create_incident,
    get_incident,
    list_incidents,
    update_incident,
)
from schemas.incident import (
    IncidentAIAnalysisRequest,
    IncidentAIAnalysisResponse,
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
)
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
    "/api/v1/incidents",
    response_model=IncidentResponse,
    status_code=201,
)
async def create_incident_endpoint(
    incident_data: IncidentCreate,
    request: Request,
):
    try:
        env = request.scope["env"]

        incident = await create_incident(
            env.DB,
            title=incident_data.title,
            description=incident_data.description,
            requester=incident_data.requester,
            area=incident_data.area,
            category=incident_data.category,
            impact_users=incident_data.impact_users,
            urgency=incident_data.urgency,
        )

        return IncidentResponse.model_validate(incident)

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível criar o incidente.",
        )


@app.get(
    "/api/v1/incidents",
    response_model=list[IncidentResponse],
)
async def list_incidents_endpoint(
    request: Request,
    limit: int = Query(default=20, ge=1, le=50),
    offset: int = Query(default=0, ge=0, le=10000),
):
    try:
        env = request.scope["env"]

        incidents = await list_incidents(
            env.DB,
            limit=limit,
            offset=offset,
        )

        return [
            IncidentResponse.model_validate(incident)
            for incident in incidents
        ]

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível consultar os incidentes.",
        )


@app.get(
    "/api/v1/incidents/{incident_id}",
    response_model=IncidentResponse,
)
async def get_incident_endpoint(
    incident_id: int,
    request: Request,
):
    if incident_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="ID do incidente deve ser maior que zero.",
        )

    try:
        env = request.scope["env"]

        incident = await get_incident(
            env.DB,
            incident_id,
        )

        if incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incidente não encontrado.",
            )

        return IncidentResponse.model_validate(incident)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível consultar o incidente.",
        )


@app.patch(
    "/api/v1/incidents/{incident_id}",
    response_model=IncidentResponse,
)
async def update_incident_endpoint(
    incident_id: int,
    incident_data: IncidentUpdate,
    request: Request,
):
    if incident_id <= 0:
        raise HTTPException(
            status_code=400,
            detail="ID do incidente deve ser maior que zero.",
        )

    try:
        env = request.scope["env"]

        incident = await update_incident(
            env.DB,
            incident_id,
            status=incident_data.status,
        )

        if incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incidente não encontrado.",
            )

        return IncidentResponse.model_validate(incident)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível atualizar o incidente.",
        )


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
