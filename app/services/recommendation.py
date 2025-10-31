from __future__ import annotations

from collections import defaultdict
from typing import Iterable

from app.schemas.student import LearningPath, LearningPathStep, StudentCreate

COURSE_LIBRARY = {
    "programming": [
        ("Основы Python", "https://stepik.org/course/67", "Stepik"),
        ("Введение в машинное обучение", "https://www.coursera.org/learn/machine-learning", "Coursera"),
        ("Алгоритмы и структуры данных", "https://stepik.org/course/217", "Stepik"),
    ],
    "design": [
        ("UX/UI Design", "https://www.coursera.org/specializations/ui-ux-design", "Coursera"),
        ("Figma для начинающих", "https://stepik.org/course/170609", "Stepik"),
    ],
    "marketing": [
        ("Цифровой маркетинг", "https://www.coursera.org/specializations/digital-marketing", "Coursera"),
        ("Основы SMM", "https://stepik.org/course/149048", "Stepik"),
    ],
}

PROFESSION_LIBRARY = {
    "programming": ["Backend-разработчик", "ML-инженер", "Data Scientist"],
    "design": ["UX-исследователь", "Продуктовый дизайнер"],
    "marketing": ["Digital-маркетолог", "Контент-стратег"],
}

SOFT_SKILL_LIBRARY = {
    "programming": ["Командная работа", "Критическое мышление", "Тайм-менеджмент"],
    "design": ["Эмпатия", "Коммуникация", "Визуальное мышление"],
    "marketing": ["Навыки презентации", "Аналитическое мышление", "Креативность"],
}

DEFAULT_SOFT_SKILLS = ["Коммуникация", "Гибкость", "Самоорганизация"]


def _normalize_interests(interests: Iterable[str]) -> list[str]:
    return [interest.strip().lower() for interest in interests]


def generate_learning_path(student: StudentCreate) -> LearningPath:
    normalized_interests = _normalize_interests(student.interests)
    steps: list[LearningPathStep] = []
    topics_seen: set[str] = set()

    for interest in normalized_interests:
        for title, url, provider in COURSE_LIBRARY.get(interest, []):
            if title in topics_seen:
                continue
            steps.append(
                LearningPathStep(
                    title=title,
                    description=f"Изучи курс {title} на платформе {provider} для углубления навыков в области '{interest}'.",
                    resource=url,
                )
            )
            topics_seen.add(title)

    if not steps:
        steps.append(
            LearningPathStep(
                title="Навык самообучения",
                description="Научись ставить цели и планировать обучение, используя метод SMART.",
                resource="https://www.coursera.org/learn/learning-how-to-learn",
            )
        )

    overview = (
        "Дорожная карта сформирована на основе твоих интересов и целей. Начни с базовых курсов,"
        " затем переходи к более продвинутым модулям и закрепляй знания через проекты."
    )

    return LearningPath(overview=overview, steps=steps[:6])


def recommend_professions(student: StudentCreate) -> list[str]:
    normalized_interests = _normalize_interests(student.interests)
    professions: list[str] = []
    seen: set[str] = set()

    for interest in normalized_interests:
        for profession in PROFESSION_LIBRARY.get(interest, []):
            if profession not in seen:
                professions.append(profession)
                seen.add(profession)

    if not professions:
        professions = ["Продакт-менеджер", "Предприниматель"]

    return professions[:5]


def recommend_soft_skills(student: StudentCreate) -> list[str]:
    normalized_interests = _normalize_interests(student.interests)
    recommendations: dict[str, int] = defaultdict(int)

    for interest in normalized_interests:
        for skill in SOFT_SKILL_LIBRARY.get(interest, []):
            recommendations[skill] += 1

    if not recommendations:
        return DEFAULT_SOFT_SKILLS

    sorted_skills = sorted(recommendations.items(), key=lambda item: item[1], reverse=True)
    return [skill for skill, _ in sorted_skills][:5]
