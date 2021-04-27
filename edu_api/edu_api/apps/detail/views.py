from rest_framework.generics import RetrieveAPIView, ListAPIView

from course.models import Course, CourseChapter, CourseLesson
from detail.serializer import DetailCourseSerializer, DetailCourseChapterSerializer, CourseLessonSerializer

"""课程信息"""
class DetailCourseView(RetrieveAPIView):
    queryset = Course.objects.filter(is_show=True, is_delete=False)
    serializer_class = DetailCourseSerializer
    # 指定获取单个对象的主键的名称
    lookup_field = "id"


"""章节信息"""
class DetailCourseChapterView(ListAPIView):

    queryset = CourseChapter.objects.filter(is_show=True, is_delete=False).order_by("id")
    serializer_class = DetailCourseChapterSerializer
    # 指定获取单个对象的主键的名称
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        c_id = kwargs.get("id")
        if c_id:
            self.queryset = CourseChapter.objects.filter(is_show=True, is_delete=False, course_id=c_id).order_by("id")
        return self.list(request, *args, **kwargs)


"""课时信息"""
class CourseLessonView(ListAPIView):

    queryset = CourseLesson.objects.filter(is_show=True, is_delete=False).order_by("id")
    serializer_class = CourseLessonSerializer
    # 指定获取单个对象的主键的名称
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        c_id = kwargs.get("id")
        if c_id:
            self.queryset = CourseLesson.objects.filter(is_show=True, is_delete=False, chapter_id=c_id).order_by("id")
        return self.list(request, *args, **kwargs)