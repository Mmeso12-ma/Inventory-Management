from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    DATABASR_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKE_EXPIRE_MINUTES: int
    model_config = SettingsConfigDict(env_file=".env")
    class Config:
        env_file = ".env"
settings = Settings()