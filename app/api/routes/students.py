from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.models import Student, StudentProgress
from app.schemas.student import (
    StudentCreate,
    StudentProgressInfo,
    StudentProgressUpdate,
    StudentResponse,
)
from app.services import gamification as gamification_service
from app.services import recommendation as recommendation_service

router = APIRouter(prefix="/students", tags=["students"])


@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student_profile(student_in: StudentCreate, db: Session = Depends(get_db_session)):
    existing = db.query(Student).filter(Student.email == student_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Профиль с таким email уже существует")

    learning_path = recommendation_service.generate_learning_path(student_in)
    professions = recommendation_service.recommend_professions(student_in)
    soft_skills = recommendation_service.recommend_soft_skills(student_in)

    student = Student(
        name=student_in.name,
        email=student_in.email,
        interests=student_in.interests,
        strengths=student_in.strengths,
        goals=student_in.goals,
        learning_path=learning_path.dict(),
        recommended_professions=professions,
        soft_skill_recommendations=soft_skills,
    )

    db.add(student)
    db.flush()

    progress = StudentProgress(student_id=student.id, completed_courses=[], current_step="Начни с первого курса", progress_percent=0)
    db.add(progress)
    db.commit()
    db.refresh(student)

    return _build_student_response(student)


@router.get("/{student_id}", response_model=StudentResponse)
def get_student_profile(student_id: int, db: Session = Depends(get_db_session)):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")
    return _build_student_response(student)


@router.patch("/{student_id}/progress", response_model=StudentResponse)
def update_progress(
    student_id: int,
    progress_update: StudentProgressUpdate,
    db: Session = Depends(get_db_session),
):
    student = db.get(Student, student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")
    if not student.progress:
        student.progress = StudentProgress(student_id=student.id)

    progress = student.progress

    if progress_update.completed_courses is not None:
        progress.completed_courses = progress_update.completed_courses
    if progress_update.current_step is not None:
        progress.current_step = progress_update.current_step
    if progress_update.progress_percent is not None:
        progress.progress_percent = progress_update.progress_percent
    if progress_update.last_feedback is not None:
        progress.last_feedback = progress_update.last_feedback

    if progress.progress_percent >= 100:
        gamification_service.award_points(
            db,
            student=student,
            points=50,
            event_type="learning_path_completed",
            description="Завершение дорожной карты",
        )

    db.commit()
    db.refresh(student)
    return _build_student_response(student)


def _build_student_response(student: Student) -> StudentResponse:
    progress = None
    if student.progress:
        progress = StudentProgressInfo(
            completed_courses=student.progress.completed_courses or [],
            current_step=student.progress.current_step,
            progress_percent=student.progress.progress_percent,
            last_feedback=student.progress.last_feedback,
        )
    return StudentResponse(
        id=student.id,
        name=student.name,
        email=student.email,
        interests=student.interests or [],
        strengths=student.strengths or [],
        goals=student.goals or [],
        learning_path=student.learning_path,
        recommended_professions=student.recommended_professions or [],
        soft_skill_recommendations=student.soft_skill_recommendations or [],
        points=student.points,
        achievements=student.achievements or [],
        progress=progress,
        created_at=student.created_at,
        updated_at=student.updated_at,
    )
