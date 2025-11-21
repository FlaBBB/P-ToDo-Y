from typing import Optional

from pydantic import BaseModel


class GetDosenPort(BaseModel):
    id: Optional[int] = None
    nidn: Optional[str] = None
    nama: Optional[str] = None
    email: Optional[str] = None
    order_by: Optional[str] = None
    order: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
