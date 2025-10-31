from __future__ import annotations

from statistics import mean
from typing import Iterable

from sqlalchemy.orm import Session

from app.models import Student
from app.schemas.teacher import TeacherDashboardResponse, TeacherDashboardStudent
from app.schemas.student import StudentProgressInfo


def build_teacher_dashboard(db: Session) -> TeacherDashboardResponse:
    students: Iterable[Student] = db.query(Student).all()
    items: list[TeacherDashboardStudent] = []
    progress_values: list[int] = []

    for student in students:
        progress = None
        if student.progress:
            progress = StudentProgressInfo(
                completed_courses=student.progress.completed_courses or [],
                current_step=student.progress.current_step,
                progress_percent=student.progress.progress_percent,
                last_feedback=student.progress.last_feedback,
            )
            progress_values.append(student.progress.progress_percent)

        items.append(
            TeacherDashboardStudent(
                id=student.id,
                name=student.name,
                email=student.email,
                progress=progress,
                points=student.points,
                achievements=student.achievements or [],
            )
        )

    average_progress = mean(progress_values) if progress_values else 0.0

    return TeacherDashboardResponse(
        students=items,
        total_students=len(items),
        average_progress=round(average_progress, 2),
    )
