from fastapi import APIRouter, Query

from app.schemas.integration import ExternalCourseResponse
from app.services.integration import search_external_courses

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("/courses", response_model=ExternalCourseResponse)
def get_courses(interests: list[str] = Query(default_factory=list)):
    courses = search_external_courses(interests)
    return ExternalCourseResponse(courses=courses)
