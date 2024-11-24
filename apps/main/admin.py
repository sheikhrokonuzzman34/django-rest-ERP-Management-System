from django.contrib import admin

# Register your models here.

from django.contrib import admin
from apps.main.models import *

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('admission_number', 'user', 'class_section', 'is_active')
    search_fields = ('admission_number', 'user__username', 'user__first_name', 'user__last_name')
    list_filter = ('class_section', 'is_active')
    raw_id_fields = ('user',)

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'qualification', 'is_active')
    search_fields = ('employee_id', 'user__username', 'user__first_name', 'user__last_name')
    list_filter = ('is_active',)
    raw_id_fields = ('user',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ClassSection)
class ClassSectionAdmin(admin.ModelAdmin):
    list_display = ('class_name', 'section', 'class_teacher', 'academic_year')
    search_fields = ('class_name__name', 'section__name', 'class_teacher__user__username')
    list_filter = ('academic_year',)
    raw_id_fields = ('class_teacher',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'credits')
    search_fields = ('name', 'code')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'status')
    search_fields = ('student__user__username', 'student__admission_number')
    list_filter = ('status', 'date')
    raw_id_fields = ('student',)

@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('name', 'exam_type', 'start_date', 'end_date', 'academic_year', 'is_active')
    search_fields = ('name', 'academic_year')
    list_filter = ('exam_type', 'academic_year', 'is_active')

@admin.register(ExamResult)
class ExamResultAdmin(admin.ModelAdmin):
    list_display = ('exam', 'student', 'subject', 'marks_obtained', 'max_marks')
    search_fields = ('exam__name', 'student__user__username', 'subject__name')
    list_filter = ('exam', 'subject')
    raw_id_fields = ('exam', 'student', 'subject')

@admin.register(Fee)
class FeeAdmin(admin.ModelAdmin):
    list_display = ('student', 'fee_type', 'amount', 'due_date', 'status')
    search_fields = ('student__user__username', 'fee_type')
    list_filter = ('status', 'fee_type', 'due_date')
    raw_id_fields = ('student',)

