from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):

    MODE: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    GRPC_HOST: str
    GRPC_PORT: int

    SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    @property
    def get_DB_HOST(self)-> str:
        return self.DB_HOST

    @property
    def get_DB_PORT(self) -> str:
        return str(self.DB_PORT)

    @property
    def get_DB_USER(self) -> str:
        return self.DB_USER

    @property
    def get_DB_PASS(self) -> str:
        return self.DB_PASS

    @property
    def get_DB_NAME(self) -> str:
        return self.DB_NAME

    @property
    def DATABASE_URL_psycopg(self) -> str:
        return f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # model_config = SettingsConfigDict(env_file="/cfg/development/.env")

# load_dotenv()
settings = Settings()