import connexion
import six

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
    if connexion.request.is_json:
        body = Student.from_dict(connexion.request.get_json())  # noqa: E501
        return student_service.add(body)
    return 500,'error'


def delete_student(student_id):  # noqa: E501
    """Deletes a student

    Delete a single student # noqa: E501

    :param student_id: The UUID of the student
    :type student_id: 

    :rtype: object
    """

    return student_service.delete(student_id)


def get_student_by_id(student_id):  # noqa: E501
    """Gets student

    Returns a single student # noqa: E501

    :param student_id: The UUID of the student
    :type student_id:

    :rtype: Student
    """
    return student_service.get_by_id(student_id)


def get_average_grade(student_id):  # noqa: E501
    """Gets student

    Returns a single student # noqa: E501

    :param student_id: The UUID of the student
    :type student_id:

    :rtype: Student
    """
    return student_service.average_grade(student_id)