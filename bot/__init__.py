from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import SecretStr
from dotenv import load_dotenv
import pathlib


dotenv_path = pathlib.Path(__file__).parent.parent / 'config' / '.env'
load_dotenv(dotenv_path=dotenv_path)


class AppConfig(BaseSettings):
    telegram_bot_token: SecretStr
    telegram_webhook_url: Optional[str]
    telegram_webhook_port: Optional[int]
    telegram_group_id: Optional[int]

    class Config:
        env_file = 'feedbackbot/config/.env'
        env_file_encoding = 'utf-8'


config = AppConfig()
