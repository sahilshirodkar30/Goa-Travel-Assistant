
from functools import lru_cache
from typing import Literal

from pydantic import Field , SecretStr
from pydantic_settings import BaseSettings , SettingsConfigDict

class Settings(BaseSettings):
    """ This function has all the configuration need for goa travel"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False
    )

    app_env:Literal["local","production","UAT"] = "local"
    log_level:Literal["DEBUG","INFO","WARNING","ERROR"] = "INFO"

    portkey_api_key:SecretStr=Field(...,description="Portkey API key")
    portkey_base_url:str="https://api.portkey.ai/v1"
    groq_api_key:SecretStr=Field(...,description="groq api key")
    deepseek_api_key:SecretStr=Field(...,description="deepseek api key")
    llm_timeout_seconds = float=Field(default=20.0,gt=0)
    llm_max_retries:int=Field(default=1,ge=0,le=5)

    pinecone_api_key:SecretStr=Field(...,description="pinecone api key")
    pinecone_index_name:str = "goa-travel-guide-assitant"
    pinecone_namespace:str = "goa"

    logfire_token:SecretStr | None = None
    logfire_enabled: bool =True

    allowed_emails:str = Field(
        default = "",
        description="Comma-separated list of emails allowed to log in"
    )

    rate_limit_per_minute:int = Field(default=20,gt=0)
    rate_limit_per_day:int = Field(default=200,gt=0)

    @property
    def allowed_email_list(self) -> list[str]:
        return [e.strip().lower() for e in self.allowed_emails.split(",") if e.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()