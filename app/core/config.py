from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MYSQLURL:str
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    SMTP_USE_TLS: bool

    class Config:
        env_file = ".env"

settings = Settings()
