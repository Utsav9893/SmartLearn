from django.urls import path
from . import views

app_name = 'exams'

urlpatterns = [
    # Teacher views
    path('', views.exam_list, name='exam_list'),
    path('course/<int:course_pk>/create/', views.exam_create, name='exam_create'),
    path('<int:pk>/', views.exam_detail, name='exam_detail'),
    path('<int:pk>/edit/', views.exam_edit, name='exam_edit'),
    path('<int:pk>/delete/', views.exam_delete, name='exam_delete'),
    path('<int:exam_pk>/question/create/', views.question_create, name='question_create'),
    path('question/<int:pk>/edit/', views.question_edit, name='question_edit'),
    path('question/<int:pk>/delete/', views.question_delete, name='question_delete'),
    
    # Student views
    path('<int:pk>/start/', views.exam_start, name='exam_start'),
    path('<int:pk>/submit/', views.exam_submit, name='exam_submit'),
    path('<int:pk>/tab-switch/', views.exam_tab_switch, name='exam_tab_switch'),
    path('result/<int:pk>/', views.exam_result, name='exam_result'),
    path('result/<int:result_id>/pdf/', views.download_result_pdf, name='result_pdf'),
    path('results/', views.exam_results_list, name='exam_results_list'),
]

