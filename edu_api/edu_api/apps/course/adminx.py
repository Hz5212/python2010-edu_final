import xadmin

from course.models import CourseCategory, Course, Teacher, CourseChapter, CourseLesson, CourseDiscountType, \
    CourseDiscount, CoursePriceDiscount, Activity, CourseExpire

"""课程分类模型"""
class CourseCategoryModelAdmin(object):
    pass

xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)


"""课程模型"""
class CourseModelAdmin(object):
    pass

xadmin.site.register(Course, CourseModelAdmin)

"""教师分类模型"""
class TeacherModelAdmin(object):
    pass

xadmin.site.register(Teacher, TeacherModelAdmin)

"""章节模型"""
class CourseChapterModelAdmin(object):
    pass

xadmin.site.register(CourseChapter, CourseChapterModelAdmin)

"""课时模型"""
class CourseLessonModelAdmin(object):
    pass

xadmin.site.register(CourseLesson, CourseLessonModelAdmin)


# 以下是优惠活动相关
class PriceDiscountTypeModelAdmin(object):
    """价格优惠类型"""
    pass

xadmin.site.register(CourseDiscountType, PriceDiscountTypeModelAdmin)


class PriceDiscountModelAdmin(object):
    """价格优惠公式"""
    pass

xadmin.site.register(CourseDiscount, PriceDiscountModelAdmin)


class CoursePriceDiscountModelAdmin(object):
    """商品优惠和活动的关系"""
    pass

xadmin.site.register(CoursePriceDiscount, CoursePriceDiscountModelAdmin)


class ActivityModelAdmin(object):
    """商品活动模型"""
    pass

xadmin.site.register(Activity, ActivityModelAdmin)

xadmin.site.register(CourseExpire)

