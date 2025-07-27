from pydantic import BaseModel


class DBConfigurationDTO(BaseModel):
    user_name: str
    password: str
    host: str
    port: int
    database: str
    connection_string: str
