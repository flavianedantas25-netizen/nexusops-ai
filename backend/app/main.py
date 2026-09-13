from fastapi import FastAPI

from backend.app.api.incidents import router as incidents_router
from backend.app.core.database import Base, engine
from backend.app.models.incident import Incident


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="NexusOps AI",
    description="Plataforma inteligente para gestão, triagem e análise de incidentes corporativos.",
    version="0.1.0",
)


app.include_router(incidents_router)


@app.get("/")
def raiz():
    return {
        "sistema": "NexusOps AI",
        "status": "online",
        "versao": "0.1.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }
