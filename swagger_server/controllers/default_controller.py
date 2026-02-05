import connexion
import six
from flask import jsonify

from swagger_server.models.student import Student  # noqa: E501
from swagger_server import util
import swagger_server.service.student_service as student_service


def add_student(body):  # noqa: E501
    """Add a new student

    Adds an item to the system # noqa: E501

    :param body: Student item to add
    :type body: dict | bytes

    :rtype: str
    """
    if not connexion.request.is_json:
        # If request is not JSON, return 400 Bad Request
        return {"error": "Request body must be JSON"}, 400

    body = Student.from_dict(connexion.request.get_json())  # noqa: E501
    result = student_service.add(body)

    # student_service.add() could return a UUID string or a tuple like ('already exists', 409)
    if isinstance(result, tuple):
        message, status = result
        return {"error": message}, status

    # Successfully created
    return {"student_id": result, "message": "Student added successfully"}, 201

def delete_student(student_id):  # noqa: E501
    """Deletes a student

    Delete a single student # noqa: E501

    :param student_id: The UUID of the student
    :type student_id: 

    :rtype: object
    """
    result = student_service.delete(student_id)

    # Handle service response for errors
    if isinstance(result, tuple):
        # Already in form (message, status_code)
        return {"message": result[0]}, result[1]

    # Success
    return {"student_id": student_id}, 200


def get_student_by_id(student_id):  # noqa: E501
    """Gets student

    Returns a single student # noqa: E501

    :param student_id: The UUID of the student
    :type student_id:

    :rtype: Student
    """
    result = student_service.get_by_id(student_id)

    # Handle service response for errors
    if isinstance(result, tuple):
        # Already in form (message, status_code)
        return {"message": result[0]}, result[1]

    # Success, return student as JSON
    return result, 200
