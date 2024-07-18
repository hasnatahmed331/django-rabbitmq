from rest_framework import serializers
from .models import Student, Course, Enrollment


class StudentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Student model.

    This serializer converts the Student model instance to and from various data formats such as JSON.

    Meta Attributes:
        model (Student): The model that this serializer serializes.
        fields (str): Specifies that all fields of the Student model should be included.
    """

    class Meta:
        model = Student
        fields = "__all__"


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.

    This serializer converts the Course model instance to and from various data formats such as JSON.

    Meta Attributes:
        model (Course): The model that this serializer serializes.
        fields (str): Specifies that all fields of the Course model should be included.
    """

    class Meta:
        model = Course
        fields = "__all__"


class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Enrollment model.

    This serializer converts the Enrollment model instance to and from various data formats such as JSON.

    Meta Attributes:
        model (Enrollment): The model that this serializer serializes.
        fields (str): Specifies that all fields of the Enrollment model should be included.
    """

    class Meta:
        model = Enrollment
        fields = "__all__"
