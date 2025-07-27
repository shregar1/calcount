from pydantic import BaseModel


class CacheConfigurationDTO(BaseModel):
    host: str
    port: int
    password: str
