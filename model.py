from pydantic import BaseModel, validator

class Todo(BaseModel):
    name: str
    address: str
    phone: str

class TodoResponse(BaseModel):
    id: int
    name: str
    address: str
    phone: str

    @validator("id", pre=True)
    def parse_id(cls, value):
        return int(value)
