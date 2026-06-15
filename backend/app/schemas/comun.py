from pydantic import BaseModel


class SelectOption(BaseModel):
    value: int
    label: str
