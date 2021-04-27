from django.urls import path

from course import views

urlpatterns = [
    path("category/", views.CourseCategoryView.as_view()),
    path("list/", views.CourseListAPIView.as_view()),

]