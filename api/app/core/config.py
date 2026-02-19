from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str = ""
    supabase_key: str = ""
    openai_api_key: str = ""
    gmail_credentials_path: str = "./credentials/gmail.json"

    model_config = {"env_file": ".env"}


settings = Settings()
