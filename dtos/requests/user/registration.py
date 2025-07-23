from pydantic import BaseModel


class UserRegistrationRequestDTO(BaseModel):

    reference_number: str
    email: str
    password: str
