from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.core.database import get_db
from backend.app.models.incident import Incident
from backend.app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
    IncidentAIAnalysisRequest,
    IncidentAIAnalysisResponse,
)
from backend.app.services.priority import calculate_priority
from backend.app.services.classifier import (
    classify_incident,
    classify_priority,
)
from backend.app.services.ai import analyze_incident


router = APIRouter(
    prefix="/api/v1/incidents",
    tags=["Incidentes"],
)


@router.post(
    "",
    response_model=IncidentResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_incident(
    incident_data: IncidentCreate,
    db: Session = Depends(get_db),
):
    # Prioridade baseada nas regras de negócio
    priority = calculate_priority(
        incident_data.impact_users,
        incident_data.urgency,
    )

    # Classificação automática baseada nas regras atuais
    ai_category, ai_confidence = classify_incident(
        incident_data.title,
        incident_data.description,
    )

    ai_priority, _ = classify_priority(
        incident_data.impact_users,
        incident_data.urgency,
        incident_data.title,
        incident_data.description,
    )

    incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        requester=incident_data.requester,
        area=incident_data.area,
        category=incident_data.category,
        impact_users=incident_data.impact_users,
        urgency=incident_data.urgency,
        priority=priority,
        ai_category=ai_category,
        ai_priority=ai_priority,
        ai_confidence=ai_confidence,
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

    return incident


@router.post(
    "/analyze",
    response_model=IncidentAIAnalysisResponse,
)
def analyze_incident_with_ai(
    incident_data: IncidentAIAnalysisRequest,
):
    try:
        analysis = analyze_incident(
            incident_data.title,
            incident_data.description,
        )

        return IncidentAIAnalysisResponse(
            title=incident_data.title,
            description=incident_data.description,
            analysis=analysis,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Não foi possível realizar a análise com IA: {exc}",
        )


@router.get(
    "",
    response_model=list[IncidentResponse],
)
def list_incidents(
    db: Session = Depends(get_db),
):
    query = select(Incident).order_by(Incident.created_at.desc())

    return db.scalars(query).all()


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse,
)
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db),
):
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incidente não encontrado.",
        )

    return incident


@router.patch(
    "/{incident_id}",
    response_model=IncidentResponse,
)
def update_incident(
    incident_id: int,
    incident_data: IncidentUpdate,
    db: Session = Depends(get_db),
):
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incidente não encontrado.",
        )

    allowed_statuses = {
        "aberto",
        "em_atendimento",
        "resolvido",
        "encerrado",
    }

    if incident_data.status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Status inválido. "
                "Use: aberto, em_atendimento, resolvido ou encerrado."
            ),
        )

    incident.status = incident_data.status

    db.commit()
    db.refresh(incident)

    return incident
