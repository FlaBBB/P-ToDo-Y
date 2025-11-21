from typing import Optional
from pydantic import BaseModel


class GetMataKuliahPort(BaseModel):
    id: Optional[int] = None
    kode_mk: Optional[str] = None
    nama_mk: Optional[str] = None
    sks: Optional[int] = None
    order_by: Optional[str] = None
    order: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
