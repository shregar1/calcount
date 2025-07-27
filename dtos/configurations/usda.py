from pydantic import BaseModel


class USDAConfigurationDTO(BaseModel):
    url: str
