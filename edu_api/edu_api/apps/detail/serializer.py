from rest_framework.serializers import ModelSerializer

from course.models import Course, Teacher, CourseChapter, CourseLesson

"""教师信息序列化器"""
class TeacherModelSerializer(ModelSerializer):

    class Meta:
        model = Teacher
        fields = ["id", "name", "title", "image", "brief"]


"""章节信息序列化器"""
class DetailCourseChapterSerializer(ModelSerializer):

    class Meta:
        model = CourseChapter
        fields = ["id", "name", "chapter", "course_id", "lesson_list", "active_time"]


"""课时信息序列化器"""
class CourseLessonSerializer(ModelSerializer):

    class Meta:
        model = CourseLesson
        fields = ["id", "name", "orders", "free_trail"]


"""课程信息序列化器"""
class DetailCourseSerializer(ModelSerializer):

    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "students", "lessons", "pub_lessons",
                  "level", "level_choices", "price", "teacher", "discount_name",
                  "real_price", "active_time"]


