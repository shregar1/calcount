from pydantic import BaseModel
from typing import List, Dict, Union, Optional


class BaseResponseDTO(BaseModel):

    transactionUrn: str
    status: str
    responseMessage: str
    responseKey: str
    data: Optional[Union[List, Dict]] = None
    errors: Optional[Union[List, Dict]] = None
