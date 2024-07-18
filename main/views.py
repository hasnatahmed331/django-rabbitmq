from rest_framework import generics, status
from rest_framework.response import Response
from .models import Student, Course, Enrollment
from .serializers import StudentSerializer, CourseSerializer, EnrollmentSerializer
from utils.backup import BackupManager
from .throttle import RoleBasedRateThrottle
from .rabbit_mq import publish_message
import json


# Student Views
class StudentListView(generics.ListAPIView):
    """
    API view to retrieve a list of students.
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single student by ID.
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentCreateView(generics.CreateAPIView):
    """
    API view to create a new student.
    Throttled based on user role.
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    throttle_classes = [RoleBasedRateThrottle]

    def perform_create(self, serializer):
        """
        Custom behavior for creating a student.
        Publishes a message to the 'student_queue' and initiates backup.
        """
        super().perform_create(serializer)
        student = serializer.instance  # Access the created student instance
        message = json.dumps({"id": student.id, "email": student.email})
        publish_message("student_queue", message)
        BackupManager()


class StudentUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing student.
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class StudentDeleteView(generics.DestroyAPIView):
    """
    API view to delete a student.
    """

    queryset = Student.objects.all()
    serializer_class = StudentSerializer


# Course Views
class CourseListView(generics.ListAPIView):
    """
    API view to retrieve a list of courses.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDetailView(generics.RetrieveAPIView):
    """
    API view to retrieve a single course by ID.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseCreateView(generics.CreateAPIView):
    """
    API view to create a new course.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseUpdateView(generics.UpdateAPIView):
    """
    API view to update an existing course.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class CourseDeleteView(generics.DestroyAPIView):
    """
    API view to delete a course.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer


# Enrollment Views
class EnrollmentListView(generics.ListAPIView):
    """
    API view to retrieve a list of enrollments.
    """

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class EnrollStudentView(generics.CreateAPIView):
    """
    API view to enroll a student in a course.
    Validates the existence of the student and course before creating an enrollment.
    """

    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer

    def create(self, request, *args, **kwargs):
        """
        Custom behavior for enrolling a student in a course.
        Validates the student and course IDs before creating the enrollment.
        """
        student_id = request.data.get("student_id")
        course_id = request.data.get("course_id")

        try:
            student = Student.objects.get(pk=student_id)
        except Student.DoesNotExist:
            return Response(
                {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
            )

        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response(
                {"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND
            )

        enrollment = Enrollment(student=student, course=course)
        enrollment.save()
        serializer = self.get_serializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
