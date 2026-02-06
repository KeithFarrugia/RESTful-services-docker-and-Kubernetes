import os
import tempfile
import time
import uuid
from pymongo import MongoClient, errors
from functools import reduce

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

    # Make sure you store grades as a list of numbers
    doc = student.to_dict()
    if "grade_records" in doc:
        doc["grades"] = [g["grade"] for g in doc["grade_records"]]
        del doc["grade_records"]

    students_col.insert_one(doc)
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