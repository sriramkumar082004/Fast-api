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


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserLogin(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: str | None = None
