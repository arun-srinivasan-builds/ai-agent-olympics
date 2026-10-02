from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    openai_api_key: str
    serper_api_key: str
    model: str
    eval_model: str

    @property
    def ready(self) -> bool:
        return bool(self.openai_api_key and self.serper_api_key)


def get_settings() -> Settings:
    model = os.getenv("AI_MODEL", "gpt-4.1-mini").strip() or "gpt-4.1-mini"
    return Settings(
        openai_api_key=os.getenv("OPENAI_API_KEY", "").strip(),
        serper_api_key=os.getenv("SERPER_API_KEY", "").strip(),
        model=model,
        eval_model=os.getenv("EVAL_MODEL", model).strip() or model,
    )
