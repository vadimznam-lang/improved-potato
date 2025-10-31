from __future__ import annotations

from typing import Iterable

from app.schemas.integration import ExternalCourse

EXTERNAL_COURSES = [
    ExternalCourse(
        provider="Stepik",
        title="Анализ данных в Python",
        url="https://stepik.org/course/4852",
        tags=["programming", "data", "analytics"],
    ),
    ExternalCourse(
        provider="Coursera",
        title="Креативный маркетинг",
        url="https://www.coursera.org/specializations/creative-marketing",
        tags=["marketing", "creativity"],
    ),
    ExternalCourse(
        provider="Stepik",
        title="Основы графического дизайна",
        url="https://stepik.org/course/103588",
        tags=["design", "visual"],
    ),
]


def search_external_courses(interests: Iterable[str]) -> list[ExternalCourse]:
    normalized = {interest.lower() for interest in interests}
    matched = [
        course for course in EXTERNAL_COURSES if normalized.intersection({tag.lower() for tag in course.tags})
    ]
    if matched:
        return matched
    return EXTERNAL_COURSES[:3]
