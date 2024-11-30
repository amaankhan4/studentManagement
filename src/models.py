from pydantic import BaseModel, Field
from typing import List

class Address(BaseModel):
    city : str
    country : str

class Student(BaseModel):
    name : str
    age : int
    address : Address

class StudentResponse(BaseModel):
    name : str
    age : int
    address : Address

class Studentsdn(BaseModel):
    name : str
    age : int

class StudentList(BaseModel):
    data : List[Studentsdn]


