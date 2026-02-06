import os
import tempfile
import uuid
from functools import reduce

from tinydb import TinyDB, Query

db_dir_path = os.path.join(os.path.dirname(__file__), "tmp")
os.makedirs(db_dir_path, exist_ok=True)
db_file_path = os.path.join(db_dir_path, "students.json")
student_db = TinyDB(db_file_path)
print("TinyDB is using file:", db_file_path)  # <-- print the path

def add(student=None):
    queries = []
    query = Query()
    queries.append(query.first_name == student.first_name)
    queries.append(query.last_name == student.last_name)
    query = reduce(lambda a, b: a & b, queries)
    res = student_db.search(query)
    if res:
        return 'already exists', 409

    student.student_id = str(uuid.uuid4())

    student_db.insert(student.to_dict())
    return {"student_id": student.student_id}, 200


def get_by_id(student_id=None, subject=None):
    student = student_db.get(Query().student_id == student_id)
    if not student:
        return 'not found', 404
    student['student_id'] = student_id
    print(student)
    return student_id, 200


def delete(student_id=None):
    student = student_db.get(Query().student_id == student_id)
    if not student:
        return 'not found', 404
    student_db.remove(Query().student_id == student_id)
    return student_id
