from app.schemas.student import StudentCreate
from app.services import recommendation


def test_generate_learning_path_for_programming_interest():
    student = StudentCreate(
        name="Иван",
        email="ivan@example.com",
        interests=["Programming"],
        strengths=["Математика"],
        goals=["Поступить в вуз"],
    )
    learning_path = recommendation.generate_learning_path(student)
    assert learning_path.steps, "Должны быть сгенерированы шаги"
    assert any("Python" in step.title for step in learning_path.steps)


def test_recommend_professions_default():
    student = StudentCreate(
        name="Анна",
        email="anna@example.com",
        interests=[],
        strengths=["Коммуникация"],
        goals=["Развитие soft skills"],
    )
    professions = recommendation.recommend_professions(student)
    assert professions == ["Продакт-менеджер", "Предприниматель"]
