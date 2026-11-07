from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


    openai_api_key: str = "0"     #поставить 0 если используется GigaChat
    openai_base_url: str = "http://localhost:8090/v1"
    llm_model: str = "GigaChat-3-Ultra"
    embedding_model: str = "text-embedding-3-small"

    course_materials_path: str = "data/course_materials.txt"
    students_csv_path: str = "data/students.csv"

settings = Settings()