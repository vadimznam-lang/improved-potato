from fastapi import FastAPI

from app.api.routes import gamification, integrations, students, teachers
from app.core.config import get_settings
from app.db.base import Base
from app.db.session import engine

Base.metadata.create_all(bind=engine)

settings = get_settings()

app = FastAPI(title=settings.app_name)

app.include_router(students.router)
app.include_router(teachers.router)
app.include_router(gamification.router)
app.include_router(integrations.router)


@app.get("/")
def healthcheck():
    return {"status": "ok", "app": settings.app_name}
