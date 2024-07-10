from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
import uuid
from pydantic import BaseModel
from pydantic import StrictStr


class Base(BaseModel):
    reference_id: Optional[str] = str(uuid.uuid4())
    created_by: str = 'MQTT'
    created_at: datetime = datetime.utcnow()
    updated_by: Optional[str] = None
    updated_at: Optional[datetime] = None
