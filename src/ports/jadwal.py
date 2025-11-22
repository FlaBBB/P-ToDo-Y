from datetime import time
from typing import Optional
from pydantic import BaseModel

class GetJadwalPort(BaseModel):
    id: Optional[int] = None
    hari: Optional[str] = None
    jam_mulai: Optional[time] = None
    jam_selesai: Optional[time] = None
    ruangan: Optional[str] = None
    mata_kuliah_id: Optional[int] = None
    dosen_id: Optional[int] = None
    order_by: Optional[str] = None
    order: Optional[str] = None
    limit: Optional[int] = None
    page: Optional[int] = None
