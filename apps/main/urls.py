from django.urls import path
from . import views



urlpatterns = [
    # Student Management URLs
    path('students/', views.student_list, name='student-list'),
    path('students/<int:pk>/', views.student_detail, name='student-detail'),

    # Teacher Management URLs
    path('teachers/', views.teacher_list, name='teacher-list'),

    # Class Management URLs
    path('class-sections/', views.class_section_list, name='class-section-list'),

    # Attendance Management URLs
    path('attendance/mark/', views.mark_attendance, name='mark-attendance'),
    path('attendance/report/', views.get_attendance_report, name='attendance-report'),

    # Exam Management URLs
    path('exams/', views.exam_management, name='exam-management'),
    path('exams/results/add/', views.add_exam_result, name='add-exam-result'),
    path('exams/results/', views.get_exam_results, name='get-exam-results'),

    # Fee Management URLs
    path('fees/', views.fee_management, name='fee-management'),
    path('fees/payment/', views.record_fee_payment, name='record-fee-payment'),

    # Dashboard URL
    path('dashboard/', views.dashboard_summary, name='dashboard-summary'),
]