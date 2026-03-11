from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Party Planner API"
    app_env: str = "development"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    database_url: str
    nominatim_base_url: str = "https://nominatim.openstreetmap.org"
    nominatim_user_agent: str

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)


settings = Settings()
