from typing import Final, Optional
from dotenv import load_dotenv
import os

class Config:
    def __init__(self, env_path: Optional[str] = None):
        if env_path:
            load_dotenv(dotenv_path=env_path)
        else:
            load_dotenv() # Load from default .env location

        self.DATABASE_URL: Final[str] = os.getenv("DB_URL", "sqlite:///./mahasiswa.db")
