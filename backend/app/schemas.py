from pydantic import BaseModel


class StudentBase(BaseModel):
    name: str
    email: str
    age: int


class StudentCreate(StudentBase):
    pass


class StudentUpdate(StudentBase):
    id: int

class Config:
    from_attributes = True


class StudentResponse(StudentBase):
    id: int

class Config:
    from_attributes = True

