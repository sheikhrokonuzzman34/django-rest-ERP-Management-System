# serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from datetime import datetime

from .models import (
    Student, Teacher, Class, Section, ClassSection, 
    Subject, Attendance, Exam, ExamResult, Fee
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone_number', 'role')
        read_only_fields = ('id', 'email')

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class_section_name = serializers.SerializerMethodField()
    attendance_percentage = serializers.SerializerMethodField()
    pending_fees = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = (
            'id', 'user', 'admission_number', 'roll_number', 'date_of_birth',
            'gender', 'address', 'guardian_name', 'guardian_phone',
            'guardian_email', 'class_section', 'class_section_name',
            'admission_date', 'is_active', 'attendance_percentage',
            'pending_fees'
        )
        read_only_fields = ('id', 'admission_date', 'attendance_percentage', 'pending_fees')

    def get_class_section_name(self, obj):
        return f"{obj.class_section.class_name.name} - {obj.class_section.section.name}"

    def get_attendance_percentage(self, obj):
        total_days = Attendance.objects.filter(student=obj).count()
        if total_days == 0:
            return 0
        present_days = Attendance.objects.filter(student=obj, status='P').count()
        return round((present_days / total_days) * 100, 2)

    def get_pending_fees(self, obj):
        return Fee.objects.filter(student=obj, status='PEN').count()

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    subjects_detail = serializers.SerializerMethodField()
    class_sections = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = (
            'id', 'user', 'employee_id', 'qualification',
            'experience_years', 'subjects', 'subjects_detail',
            'class_sections', 'date_joined', 'is_active'
        )
        read_only_fields = ('id', 'date_joined')

    def get_subjects_detail(self, obj):
        return [{'id': subject.id, 'name': subject.name} for subject in obj.subjects.all()]

    def get_class_sections(self, obj):
        class_sections = ClassSection.objects.filter(class_teacher=obj)
        return [f"{cs.class_name.name} - {cs.section.name}" for cs in class_sections]

class ClassSerializer(serializers.ModelSerializer):
    total_students = serializers.SerializerMethodField()

    class Meta:
        model = Class
        fields = ('id', 'name', 'description', 'total_students')

    def get_total_students(self, obj):
        return Student.objects.filter(class_section__class_name=obj).count()

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ('id', 'name', 'description')

class ClassSectionSerializer(serializers.ModelSerializer):
    class_name_detail = ClassSerializer(source='class_name', read_only=True)
    section_detail = SectionSerializer(source='section', read_only=True)
    class_teacher_detail = TeacherSerializer(source='class_teacher', read_only=True)
    students_count = serializers.SerializerMethodField()

    class Meta:
        model = ClassSection
        fields = (
            'id', 'class_name', 'class_name_detail', 
            'section', 'section_detail',
            'class_teacher', 'class_teacher_detail',
            'academic_year', 'room_number', 'students_count'
        )

    def get_students_count(self, obj):
        return Student.objects.filter(class_section=obj).count()

class SubjectSerializer(serializers.ModelSerializer):
    teachers = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ('id', 'name', 'code', 'description', 'credits', 'teachers')

    def get_teachers(self, obj):
        teachers = Teacher.objects.filter(subjects=obj)
        return [f"{teacher.user.first_name} {teacher.user.last_name}" for teacher in teachers]

class AttendanceSerializer(serializers.ModelSerializer):
    student_detail = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Attendance
        fields = (
            'id', 'student', 'student_detail', 
            'date', 'status', 'status_display', 
            'remarks'
        )

    def get_student_detail(self, obj):
        return {
            'name': f"{obj.student.user.first_name} {obj.student.user.last_name}",
            'admission_number': obj.student.admission_number,
            'class_section': f"{obj.student.class_section.class_name.name} - {obj.student.class_section.section.name}"
        }

class ExamSerializer(serializers.ModelSerializer):
    exam_type_display = serializers.CharField(source='get_exam_type_display', read_only=True)
    total_students = serializers.SerializerMethodField()
    results_published = serializers.SerializerMethodField()

    class Meta:
        model = Exam
        fields = (
            'id', 'name', 'exam_type', 'exam_type_display',
            'start_date', 'end_date', 'academic_year',
            'is_active', 'total_students', 'results_published'
        )

    def get_total_students(self, obj):
        return ExamResult.objects.filter(exam=obj).values('student').distinct().count()

    def get_results_published(self, obj):
        return ExamResult.objects.filter(exam=obj).exists()

class ExamResultSerializer(serializers.ModelSerializer):
    student_detail = serializers.SerializerMethodField()
    subject_detail = serializers.SerializerMethodField()
    percentage = serializers.SerializerMethodField()
    grade = serializers.SerializerMethodField()

    class Meta:
        model = ExamResult
        fields = (
            'id', 'exam', 'student', 'student_detail',
            'subject', 'subject_detail', 'marks_obtained',
            'max_marks', 'percentage', 'grade', 'remarks'
        )

    def get_student_detail(self, obj):
        return {
            'name': f"{obj.student.user.first_name} {obj.student.user.last_name}",
            'admission_number': obj.student.admission_number,
            'class_section': f"{obj.student.class_section.class_name.name} - {obj.student.class_section.section.name}"
        }

    def get_subject_detail(self, obj):
        return {
            'name': obj.subject.name,
            'code': obj.subject.code
        }

    def get_percentage(self, obj):
        return round((obj.marks_obtained / obj.max_marks) * 100, 2)

    def get_grade(self, obj):
        percentage = self.get_percentage(obj)
        if percentage >= 90:
            return 'A+'
        elif percentage >= 80:
            return 'A'
        elif percentage >= 70:
            return 'B'
        elif percentage >= 60:
            return 'C'
        elif percentage >= 50:
            return 'D'
        else:
            return 'F'

class FeeSerializer(serializers.ModelSerializer):
    student_detail = serializers.SerializerMethodField()
    fee_type_display = serializers.CharField(source='get_fee_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    is_overdue = serializers.SerializerMethodField()

    class Meta:
        model = Fee
        fields = (
            'id', 'student', 'student_detail', 'fee_type',
            'fee_type_display', 'amount', 'due_date',
            'paid_date', 'status', 'status_display',
            'payment_method', 'receipt_number', 'is_overdue'
        )
        read_only_fields = ('is_overdue',)

    def get_student_detail(self, obj):
        return {
            'name': f"{obj.student.user.first_name} {obj.student.user.last_name}",
            'admission_number': obj.student.admission_number,
            'class_section': f"{obj.student.class_section.class_name.name} - {obj.student.class_section.section.name}"
        }

    def get_is_overdue(self, obj):
        if obj.status == 'PEN' and obj.due_date < datetime.now().date():
            return True
        return False

class StudentAttendanceReportSerializer(serializers.Serializer):
    total_days = serializers.IntegerField()
    present_days = serializers.IntegerField()
    absent_days = serializers.IntegerField()
    late_days = serializers.IntegerField()
    attendance_percentage = serializers.FloatField()
    monthly_report = serializers.DictField()

class StudentFeeSummarySerializer(serializers.Serializer):
    total_fees = serializers.DecimalField(max_digits=10, decimal_places=2)
    paid_fees = serializers.DecimalField(max_digits=10, decimal_places=2)
    pending_fees = serializers.DecimalField(max_digits=10, decimal_places=2)
    overdue_fees = serializers.DecimalField(max_digits=10, decimal_places=2)
    payment_history = FeeSerializer(many=True)

class StudentAcademicReportSerializer(serializers.Serializer):
    student_detail = StudentSerializer()
    attendance_summary = StudentAttendanceReportSerializer()
    fee_summary = StudentFeeSummarySerializer()
    exam_results = ExamResultSerializer(many=True)
    class_rank = serializers.IntegerField()
    overall_grade = serializers.CharField()