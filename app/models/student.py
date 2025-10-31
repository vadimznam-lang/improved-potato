from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    interests: Mapped[List[str]] = mapped_column(JSON, default=list)
    strengths: Mapped[List[str]] = mapped_column(JSON, default=list)
    goals: Mapped[List[str]] = mapped_column(JSON, default=list)
    learning_path: Mapped[dict] = mapped_column(JSON, default=dict)
    recommended_professions: Mapped[List[str]] = mapped_column(JSON, default=list)
    soft_skill_recommendations: Mapped[List[str]] = mapped_column(JSON, default=list)
    points: Mapped[int] = mapped_column(Integer, default=0)
    achievements: Mapped[List[str]] = mapped_column(JSON, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    progress: Mapped[Optional["StudentProgress"]] = relationship(
        back_populates="student", cascade="all, delete-orphan", uselist=False
    )
    comments: Mapped[List["TeacherComment"]] = relationship(
        back_populates="student", cascade="all, delete-orphan"
    )


class StudentProgress(Base):
    __tablename__ = "student_progress"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True)
    completed_courses: Mapped[List[str]] = mapped_column(JSON, default=list)
    current_step: Mapped[str] = mapped_column(String(255), default="")
    progress_percent: Mapped[int] = mapped_column(Integer, default=0)
    last_feedback: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    student: Mapped[Student] = relationship(back_populates="progress")


class TeacherComment(Base):
    __tablename__ = "teacher_comments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    student: Mapped[Student] = relationship(back_populates="comments")
    teacher: Mapped["Teacher"] = relationship(back_populates="comments")
