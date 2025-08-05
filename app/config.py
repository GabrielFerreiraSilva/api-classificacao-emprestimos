from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PIPELINE_PATH: str = "artifacts/random_forest_class_weight_pipeline.joblib"

    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore'
    )

settings = Settings()