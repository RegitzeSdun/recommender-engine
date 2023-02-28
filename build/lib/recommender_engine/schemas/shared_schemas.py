from pydantic import BaseModel


class NextPageToken(BaseModel):
    call_id: str
    date: str
