from pydantic import BaseModel


class StudentBase(BaseModel):
    name: str
    age: int
    course: str


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


class AadhaarData(BaseModel):
    name: str | None = None
    dob: str | None = None
    gender: str | None = None
    aadhaar_number: str | None = None
