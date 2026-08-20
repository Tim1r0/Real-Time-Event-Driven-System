from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = 'localhost'
    port: int = 8080

class RabbitConfig(BaseModel):
    host: str = 'localhost'
    port: int = 5672
    user: str = 'guest'
    password: str = 'guest'

    @property
    def url(self):
        return f"amqp://{self.user}:{self.password}@{self.host}:{self.port}/"

class RedisConfig(BaseModel):
    host: str = 'localhost'
    port: int = 6379

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        case_sensitive=False,
        env_nested_delimiter='__',
        env_prefix='SRC_CONFIG_',
    )
    run: RunConfig = RunConfig()
    redis: RedisConfig = RedisConfig()
    rabbit: RabbitConfig = RabbitConfig()

settings = Settings()