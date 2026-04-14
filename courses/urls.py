from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    # Teacher views
    path('', views.course_list, name='course_list'),
    path('create/', views.course_create, name='course_create'),
    path('<int:pk>/', views.course_detail, name='course_detail'),
    path('<int:pk>/report/', views.course_report_excel, name='course_report_excel'),
    path('<int:pk>/edit/', views.course_edit, name='course_edit'),
    path('<int:pk>/delete/', views.course_delete, name='course_delete'),
    path('<int:course_pk>/lesson/create/', views.lesson_create, name='lesson_create'),
    path('lesson/<int:pk>/edit/', views.lesson_edit, name='lesson_edit'),
    path('lesson/<int:pk>/delete/', views.lesson_delete, name='lesson_delete'),
    
    # Student views
    path('browse/', views.course_browse, name='course_browse'),
    path('<int:pk>/details/', views.course_detail_browse, name='course_detail_browse'),
    path('<int:pk>/enroll/', views.course_enroll, name='course_enroll'),
    path('<int:pk>/view/', views.course_view, name='course_view'),
    path('<int:course_id>/feedback/', views.submit_feedback, name='submit_feedback'),
    path('certificate/<int:course_id>/', views.generate_certificate, name='certificate'),
    path('lesson/<int:pk>/view/', views.lesson_view, name='lesson_view'),
]

