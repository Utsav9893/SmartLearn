from django.contrib import admin
from .models import Exam, Question, ExamResult, StudentAnswer


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ['title', 'course', 'duration_minutes', 'total_marks', 'is_published', 'created_at']
    list_filter = ['is_published', 'created_at']
    search_fields = ['title', 'course__title']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'exam', 'correct_answer', 'marks', 'order']
    list_filter = ['exam']
    search_fields = ['question_text']


@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ['student', 'exam', 'score', 'total_marks', 'percentage', 'is_failed_due_to_violation', 'tab_switch_warnings', 'submitted_at']
    list_filter = ['is_completed', 'is_failed_due_to_violation', 'submitted_at']
    search_fields = ['student__username', 'exam__title']
    readonly_fields = ['percentage']


@admin.register(StudentAnswer)
class StudentAnswerAdmin(admin.ModelAdmin):
    list_display = ['exam_result', 'question', 'selected_answer', 'is_correct', 'marks_obtained']
    list_filter = ['is_correct']
    search_fields = ['exam_result__student__username', 'question__question_text']
