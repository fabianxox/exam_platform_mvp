from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    DATABASE_URL: str

#on hosting we will set the psql path and all secrets directly there, while local test the lines below are needed
  #  model_config = SettingsConfigDict(
   #     env_file=".env"
    #) 


settings = Settings()