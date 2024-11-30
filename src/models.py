from pydantic import BaseModel, Field

class Address(BaseModel):
    city : str
    country : str

class Student(BaseModel):
    name : str
    age : int
    address : Address

class StudentResponse(BaseModel):
    id : str = Field(..., alias="id")
    name : str
    age : int
    address : Address

class StudentList(BaseModel):
    name : str
    age : int

