from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.agent_routes import router as agent_router
from src.api.kpi_routes import router as kpi_router
from src.api.requests_routes import router as requests_router
from src.api.upload_routes import router as upload_router
from src.config.database import init_db
from src.config.settings import get_settings

settings = get_settings()

app = FastAPI(title=settings.app_name)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router)
app.include_router(requests_router)
app.include_router(kpi_router)
app.include_router(agent_router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
