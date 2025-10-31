from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db_session
from app.models import Student, StudentProgress, Teacher, TeacherComment
from app.schemas.teacher import (
    TeacherCommentCreate,
    TeacherCreate,
    TeacherDashboardResponse,
    TeacherResponse,
)
from app.services.reporting import build_teacher_dashboard

router = APIRouter(prefix="/teachers", tags=["teachers"])


@router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
def create_teacher(teacher_in: TeacherCreate, db: Session = Depends(get_db_session)):
    existing = db.query(Teacher).filter(Teacher.email == teacher_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Преподаватель уже существует")
    teacher = Teacher(name=teacher_in.name, email=teacher_in.email)
    db.add(teacher)
    db.commit()
    db.refresh(teacher)
    return teacher


@router.get("/dashboard", response_model=TeacherDashboardResponse)
def get_dashboard(db: Session = Depends(get_db_session)):
    return build_teacher_dashboard(db)


@router.post("/{teacher_id}/comments", status_code=status.HTTP_201_CREATED)
def add_comment(
    teacher_id: int,
    comment_in: TeacherCommentCreate,
    db: Session = Depends(get_db_session),
):
    teacher = db.get(Teacher, teacher_id)
    if not teacher:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Преподаватель не найден")

    student = db.get(Student, comment_in.student_id)
    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Студент не найден")

    comment = TeacherComment(
        student_id=student.id,
        teacher_id=teacher.id,
        comment=comment_in.comment,
    )
    db.add(comment)

    if not student.progress:
        student.progress = StudentProgress(student_id=student.id)
    student.progress.last_feedback = comment_in.comment

    db.commit()
    return {"status": "ok"}
