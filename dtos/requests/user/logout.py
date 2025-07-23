from pydantic import BaseModel


class UserLogoutRequestDTO(BaseModel):

    reference_number: str
