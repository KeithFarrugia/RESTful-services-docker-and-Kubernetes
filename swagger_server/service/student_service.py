import os
import tempfile
import uuid
from pymongo import MongoClient
from functools import reduce

from tinydb import TinyDB, Query
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)


db_name = os.getenv("DB_NAME", "student_db")
db = client[db_name]
students_col = db["students"]

def add(student=None):
    if students_col.find_one({"first_name": student.first_name, "last_name": student.last_name}):
        return "already exists", 409

    student_id = str(uuid.uuid4())
    student.student_id = student_id

    students_col.insert_one(student.to_dict())
    return student_id, 200


def get_by_id(student_id=None):
    student = students_col.find_one({"student_id": student_id})
    if not student:
        return "not found", 404
    return student, 200


def delete(student_id=None):
    res = students_col.delete_one({"student_id": student_id})
    if res.deleted_count == 0:
        return "not found", 404
    return student_id, 200


def get_average_grade(student_id=None):
    student = students_col.find_one({"student_id": student_id})
    if not student:
        return "not found", 404

    grades = student.get("grades", [])
    if not grades:
        return "no grades", 404

    average = sum(grades) / len(grades)
    return {"average_grade": average}, 200