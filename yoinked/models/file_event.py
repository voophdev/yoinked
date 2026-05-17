from enum import Enum
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EventType(str, Enum):
    sort = "sort"
    retention = "retention"
    watcher = "watcher"


class FileEvent(BaseModel):
    type: EventType          # sort | retention | watcher | etc.
    action: str              # move | archive | create | delete
    file: str

    source: Optional[str] = None
    destination: Optional[str] = None

    rule: Optional[str] = None
    match: Optional[str] = None

    status: Optional[bool] = None

    timestamp: datetime = datetime.utcnow()
