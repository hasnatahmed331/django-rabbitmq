from django.urls import path
from . import views

urlpatterns = [
    path("students/", views.StudentListView.as_view(), name="list-students"),
    path(
        "students/<int:pk>/", views.StudentDetailView.as_view(), name="retrieve-student"
    ),
    path("students/create/", views.StudentCreateView.as_view(), name="create-student"),
    path(
        "students/update/<int:pk>/",
        views.StudentUpdateView.as_view(),
        name="update-student",
    ),
    path(
        "students/delete/<int:pk>/",
        views.StudentDeleteView.as_view(),
        name="delete-student",
    ),
    path("courses/", views.CourseListView.as_view(), name="list-courses"),
    path("courses/<int:pk>/", views.CourseDetailView.as_view(), name="retrieve-course"),
    path("courses/create/", views.CourseCreateView.as_view(), name="create-course"),
    path(
        "courses/update/<int:pk>/",
        views.CourseUpdateView.as_view(),
        name="update-course",
    ),
    path(
        "courses/delete/<int:pk>/",
        views.CourseDeleteView.as_view(),
        name="delete-course",
    ),
    path("enrollments/", views.EnrollmentListView.as_view(), name="list-enrollments"),
    path(
        "enrollments/enroll/", views.EnrollStudentView.as_view(), name="enroll-student"
    ),
]
