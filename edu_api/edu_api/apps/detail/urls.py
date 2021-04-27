from django.urls import path

from detail import views

urlpatterns = [
    # 当前课程信息
    path("course/<str:id>/", views.DetailCourseView.as_view()),
    # 所有课程章节课时
    path("chapter/", views.DetailCourseChapterView.as_view()),
    # 当前课程章节课时
    path("chapter/<str:id>/", views.DetailCourseChapterView.as_view()),

    # 单查课时
    path("lesson/", views.CourseLessonView.as_view()),
    path("lesson/<str:id>/", views.CourseLessonView.as_view()),
]