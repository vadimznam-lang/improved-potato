from typing import List

from pydantic import BaseModel


class ExternalCourse(BaseModel):
    provider: str
    title: str
    url: str
    tags: List[str]


class ExternalCourseResponse(BaseModel):
    courses: List[ExternalCourse]
