from pydantic import EmailStr, field_validator

from dtos.requests.abstraction import IRequestDTO


class UserRegistrationRequestDTO(IRequestDTO):

    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not v or not v.strip():
            raise ValueError('Password cannot be empty.')
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long.')
        return v
