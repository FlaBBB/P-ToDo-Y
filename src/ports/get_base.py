from abc import ABC
from dataclasses import dataclass


from typing import Optional

@dataclass
class GetBasePort(ABC):
    order_by: Optional[str] = None
    order: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
