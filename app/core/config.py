from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "EduPath.AI"
    database_url: str = "sqlite:///./edupath.db"
    external_course_providers: tuple[str, ...] = ("Stepik", "Coursera")

    class Config:
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()
