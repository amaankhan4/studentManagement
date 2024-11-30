from fastapi import FastAPI, HTTPException, Path, Query, Body
from typing import Optional, List
from bson import ObjectId
from pymongo import MongoClient
from dotenv import dotenv_values
import models

config = dotenv_values(".env")

app = FastAPI()
conn = MongoClient(config['MONGO_URI'])
db = conn.students
studentCollection = db.student

@app.post('/students', status_code=201, response_model=dict)
async def createStudent(student : models.Student):
    data = student.dict()
    result = studentCollection.insert_one(data)
    return {"id": str(result.inserted_id)}

@app.get('/students', status_code=200, response_model=List[models.StudentList])
async def getStudentData(country : Optional[str] = Query(None), age : Optional[int] = Query(None)):
    query = {}
    if country:
        query["address.country"] = country

    if age:
        query["age"] = age
    
    students = list(studentCollection.find(query,{"_id":0, "name":1, "age":1}))
    return students
