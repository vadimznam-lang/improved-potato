from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import GamificationEvent, Student

ACHIEVEMENT_THRESHOLDS = [
    (100, "Новичок в прогрессе"),
    (250, "Уверенный исследователь"),
    (500, "Лидер обучения"),
    (1000, "Амбассадор EduPath.AI"),
]


def award_points(
    db: Session, *, student: Student, points: int, event_type: str, description: str = ""
) -> GamificationEvent:
    student.points += points
    _update_achievements(student)
    event = GamificationEvent(
        student_id=student.id,
        points=points,
        event_type=event_type,
        description=description,
    )
    db.add(event)
    db.flush()
    return event


def _update_achievements(student: Student) -> None:
    earned = set(student.achievements or [])
    for threshold, achievement in ACHIEVEMENT_THRESHOLDS:
        if student.points >= threshold and achievement not in earned:
            earned.add(achievement)
    student.achievements = sorted(earned)


def get_leaderboard(db: Session, limit: int = 10) -> list[Student]:
    stmt = select(Student).order_by(Student.points.desc()).limit(limit)
    return list(db.scalars(stmt))
