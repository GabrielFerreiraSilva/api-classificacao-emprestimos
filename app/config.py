import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PIPELINE_PATH: str = os.getenv("PIPELINE_PATH", "random_forest_class_weight_pipeline.joblib")

settings = Settings()