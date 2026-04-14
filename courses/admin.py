from django.contrib import admin
from .models import Course, Lesson, Enrollment, LessonCompletion


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'teacher', 'get_student_count', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'description', 'teacher__username']
    filter_horizontal = ['students']


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'lesson_type', 'order', 'created_at']
    list_filter = ['lesson_type', 'course']
    search_fields = ['title', 'course__title']


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ['student', 'course', 'enrolled_at', 'completed']
    list_filter = ['completed', 'enrolled_at']
    search_fields = ['student__username', 'course__title']


@admin.register(LessonCompletion)
class LessonCompletionAdmin(admin.ModelAdmin):
    list_display = ['student', 'lesson', 'completed_at']
    list_filter = ['completed_at']
    search_fields = ['student__username', 'lesson__title']
