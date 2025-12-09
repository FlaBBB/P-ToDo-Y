from enum import Enum

class MahasiswaStatus(str, Enum):
    ACTIVE = "active"
    DROP_OUT = "drop_out"
    GRADUATED = "graduated"
    LEAVE = "leave"

class DosenStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    LEAVE = "leave"


class StatusTugas(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELLED = "cancelled"
