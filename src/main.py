from fastapi import FastAPI, HTTPException, Path, Query
from typing import Optional, List
from bson import ObjectId
from pymongo import MongoClient
from dotenv import dotenv_values
from models import Student, StudentList, StudentResponse

config = dotenv_values(".env")

app = FastAPI()
conn = MongoClient(config['MONGO_URI'])
db = conn.students
studentCollection = db.student

@app.get('/', status_code=200)
def index():
    return {"message": "Health Check Passed"}

@app.post('/students', status_code=201, response_model=dict)
async def createStudent(student : Student):
    data = student.dict()
    result = studentCollection.insert_one(data)
    return {"id": str(result.inserted_id)}

@app.get('/students', status_code=200, response_model=List[StudentList])
async def getStudentData(country : Optional[str] = Query(None), age : Optional[int] = Query(None)):
    query = {}
    if country:
        query["address.country"] = country

    if age:
        query["age"] = {"$gte": age}
    
    students = list(studentCollection.find(query,{"_id":0, "name":1, "age":1}))
    return {"data": students}

@app.get('/students/{id}', status_code=200, response_model=StudentResponse)
def getStudentById(id : str = Path(...)):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=422, detail="Invalid ID")
    student = studentCollection.find_one({"_id":ObjectId(id)}, {"_id":0})
    if student:
        return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.patch("/students/{id}", status_code=204)
async def update_student(id: str, student: Student):
    if ObjectId.is_valid(id) == False:
        raise HTTPException(status_code=422, detail="Invalid ID")
    update_data = {k: v for k, v in student.dict(exclude_unset=True).items()}

    result = studentCollection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_data}
    )

    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")
    return None

@app.delete("/students/{id}", status_code=200)
async def delete_student(id: str):
    if ObjectId.is_valid(id) == False:
        raise HTTPException(status_code=422, detail="Invalid ID")
    result = studentCollection.delete_one({"_id": ObjectId(id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"detail": "Student deleted successfully"}
