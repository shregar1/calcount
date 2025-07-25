from typing import List, Dict, Union, Optional

from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BaseResponseDTO:

    transactionUrn: str
    status: str
    responseMessage: str
    responseKey: str
    data: Optional[Union[List, Dict]] = None
    errors: Optional[Union[List, Dict]] = None
