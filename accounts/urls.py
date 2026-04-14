from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('resend-otp/', views.resend_otp, name='resend_otp'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('change-password/', views.change_password, name='change_password'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('student-dashboard/', views.student_dashboard, name='student_dashboard'),
    path('teacher-dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-analytics-data/', views.admin_analytics_view, name='admin_analytics_data'),

    # Admin Reports (Excel downloads, admin only)
    # Student-related
    path('reports/student-enrollment/', views.report_student_enrollment, name='report_student_enrollment'),
    path('reports/course-student-list/', views.report_course_student_list, name='report_course_student_list'),
    path('reports/student-progress/', views.report_student_progress, name='report_student_progress'),
    path('reports/student-exam-performance/', views.report_student_exam, name='report_student_exam'),

    # Teacher-related
    path('reports/teacher-activity/', views.report_teacher_activity, name='report_teacher_activity'),
    path('reports/teacher-performance/', views.report_teacher_performance, name='report_teacher_performance'),
    path('reports/course-teacher/', views.report_course_teacher, name='report_course_teacher'),

    # Course-related
    path('reports/course-enrollment-summary/', views.report_course_enrollment, name='report_course_enrollment'),
    path('reports/course-completion/', views.report_course_completion, name='report_course_completion'),
    path('reports/course-revenue/', views.report_course_revenue, name='report_course_revenue'),

    # Exam-related
    path('reports/exam-results/', views.report_exam_results, name='report_exam_results'),
    path('reports/exam-pass-fail/', views.report_exam_pass_fail, name='report_exam_pass_fail'),
    path('reports/exam-score-stats/', views.report_exam_score_stats, name='report_exam_score_stats'),

    # Platform-level
    path('reports/platform-summary/', views.report_platform_summary, name='report_platform_summary'),
    path('reports/monthly-growth/', views.report_monthly_growth, name='report_monthly_growth'),
    path('reports/most-popular-course/', views.report_most_popular_course, name='report_most_popular_course'),
    path('reports/most-active-teacher/', views.report_most_active_teacher, name='report_most_active_teacher'),
]

