# EduPath.AI

MVP веб-платформа профориентации с рекомендациями нейросети и инструментами для преподавателей.

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

После запуска API доступно по адресу `http://localhost:8000`. Документация Swagger — `http://localhost:8000/docs`.

## Основные возможности

- Создание профиля ученика с интересами, сильными сторонами и целями.
- Автогенерация индивидуальной дорожной карты обучения, списка профессий и рекомендаций по soft skills.
- Панель преподавателя с прогрессом учащихся, метриками и возможностью оставлять комментарии.
- Геймификация: начисление баллов, достижения и таблица лидеров.
- Интеграция с внешними образовательными платформами (Stepik, Coursera) через модуль API.

## Структура проекта

```
app/
├── api/
│   ├── deps.py
│   └── routes/
│       ├── gamification.py
│       ├── integrations.py
│       ├── students.py
│       └── teachers.py
├── core/
│   └── config.py
├── db/
│   ├── base.py
│   └── session.py
├── main.py
├── models/
│   ├── gamification.py
│   ├── student.py
│   └── teacher.py
├── schemas/
│   ├── gamification.py
│   ├── integration.py
│   ├── student.py
│   └── teacher.py
└── services/
    ├── gamification.py
    ├── integration.py
    ├── recommendation.py
    └── reporting.py
```

Тесты находятся в каталоге `tests/`.
