from pydantic import BaseModel


class SValueAdd(BaseModel):
    core_value: str
    user_id: str
