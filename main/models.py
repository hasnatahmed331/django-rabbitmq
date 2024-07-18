from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
from datetime import date


def validate_age(value):
    """
    Validates that the age calculated from the date of birth is greater than 18.

    Args:
        value (date): The date of birth to validate.
    """
    today = date.today()
    age = (
        today.year - value.year - ((today.month, today.day) < (value.month, value.day))
    )

    if age < 18:
        raise ValidationError(_("Age must be greater than 18 years."))


class Student(models.Model):
    """
    Represents a student with a first name, last name, email, and date of birth.

    Attributes:
        first_name (str): The first name of the student.
        last_name (str): The last name of the student.
        email (str): The email address of the student, which is unique.
        date_of_birth (date): The date of birth of the student.
    """

    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(unique=True, null=False)
    date_of_birth = models.DateField(null=False, validators=[validate_age])

    def __str__(self):
        """
        Returns a string representation of the Student object.

        :return: A string in the format "{first_name} {last_name}".
        :rtype: str
        """
        return f"{self.first_name} {self.last_name}"


class Course(models.Model):
    """
    Represents a course with a title, description, start date, and end date.

    Attributes:
        title (str): The title of the course.
        description (str): A brief description of the course.
        start_date (date): The start date of the course.
        end_date (date): The end date of the course.
    """

    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=False)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    def __str__(self):
        """
        Returns a string representation of the Course object.

        :return: The title of the course.
        :rtype: str
        """
        return self.title


class Enrollment(models.Model):
    """
    Represents an enrollment of a student in a course.

    Attributes:
        student (Student): The student who is enrolled.
        course (Course): The course in which the student is enrolled.
        enrollment_date (date): The date when the enrollment was created, automatically set to the current date.
    """

    student = models.ForeignKey(Student, on_delete=models.CASCADE, null=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=False)
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")

    def __str__(self):
        """
        Returns a string representation of the Enrollment object.

        :return: A string in the format "{student} enrolled in {course}".
        :rtype: str
        """
        return f"{self.student} enrolled in {self.course}"
