from datetime import datetime
from typing import List

from pydantic import BaseModel


class GamificationEventResponse(BaseModel):
    id: int
    student_id: int
    points: int
    event_type: str
    description: str
    created_at: datetime

    class Config:
        orm_mode = True


class LeaderboardEntry(BaseModel):
    student_id: int
    name: str
    points: int
    achievements: List[str]


class PointsAward(BaseModel):
    points: int
    event_type: str
    description: str = ""
