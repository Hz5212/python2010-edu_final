from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher


"""课程分类序列化器"""
class CourseCategoryModelSerializer(ModelSerializer):

    class Meta:
        model = CourseCategory
        fields = ["id", "name"]


"""教师信息序列化器"""
class TeacherModelSerializer(ModelSerializer):

    class Meta:
        model = Teacher
        fields = ["id", "name", "title"]


"""课程信息序列化器"""
class CourseModelSerializer(ModelSerializer):

    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons",
                  "price", "teacher", "lesson_list", "course_video", "discount_name",
                  "real_price", "expire_list"]