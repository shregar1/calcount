from pydantic import BaseModel


class UserLoginRequestDTO(BaseModel):

    reference_number: str
    email: str
    password: str
