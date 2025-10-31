from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.models import Student
from app.schemas.gamification import GamificationEventResponse, LeaderboardEntry, PointsAward
from app.services.gamification import award_points, get_leaderboard

router = APIRouter(prefix="/gamification", tags=["gamification"])


@router.post("/{student_id}/award", response_model=GamificationEventResponse)
def award_points_to_student(
    student_id: int,
    payload: PointsAward,
    db: Session = Depends(get_db_session),
):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Студент не найден")

    event = award_points(
        db,
        student=student,
        points=payload.points,
        event_type=payload.event_type,
        description=payload.description,
    )
    db.commit()
    db.refresh(student)
    db.refresh(event)
    return event


@router.get("/leaderboard", response_model=list[LeaderboardEntry])
def get_leaderboard_view(db: Session = Depends(get_db_session)):
    students = get_leaderboard(db)
    return [
        LeaderboardEntry(
            student_id=student.id,
            name=student.name,
            points=student.points,
            achievements=student.achievements or [],
        )
        for student in students
    ]
