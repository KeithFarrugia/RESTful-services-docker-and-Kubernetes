import os
import tempfile
import time
import uuid
from pymongo import MongoClient, errors

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "student_db")

# Retry loop to wait for MongoDB to be ready
max_retries = 10
for i in range(max_retries):
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')  # triggers exception if Mongo is not ready
        print("Connected to MongoDB!")
        break
    except errors.ServerSelectionTimeoutError:
        print(f"MongoDB not ready ({i+1}/{max_retries})... retrying in 2s")
        time.sleep(2)
else:
    print("MongoDB connection failed after retries")
    exit(1)

db = client[DB_NAME]
students_col = db["students"]



def add(student=None):
    if students_col.find_one({"first_name": student.first_name, "last_name": student.last_name}):
        return "already exists", 409

    student_id = str(uuid.uuid4())
    student.student_id = student_id

    # Just store grade_records directly
    doc = student.to_dict()
    students_col.insert_one(doc)
    return student_id, 200


def get_by_id(student_id=None):
    student = students_col.find_one({"student_id": student_id})
    if not student:
        return "not found", 404

    # remove MongoDB _id
    student.pop("_id", None)
    return student, 200

def delete(student_id=None):
    res = students_col.delete_one({"student_id": student_id})
    if res.deleted_count == 0:
        return "not found", 404
    return student_id, 200


def average_grade(student_id=None):
    student = students_col.find_one({"student_id": student_id})
    if not student:
        return "not found", 404

    # Extract grades from grade_records
    grade_records = student.get("grade_records", [])
    if not grade_records:
        return "no grades", 404

    grades = [record.get("grade", 0) for record in grade_records]
    if not grades:
        return "no grades", 404

    average = sum(grades) / len(grades)
    return {"average_grade": average}, 200