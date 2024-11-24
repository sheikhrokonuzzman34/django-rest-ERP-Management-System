from django.db import models
from django.utils.timezone import now
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Student(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='student_profile')
    admission_number = models.CharField(max_length=20, unique=True)
    roll_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender_choices = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]
    gender = models.CharField(max_length=1, choices=gender_choices)
    address = models.TextField()
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=15)
    guardian_email = models.EmailField(blank=True, null=True)
    class_section = models.ForeignKey('ClassSection', on_delete=models.CASCADE)
    admission_date = models.DateField(default=now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.admission_number} - {self.user.first_name} {self.user.last_name}"

class Teacher(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teacher_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    qualification = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    subjects = models.ManyToManyField('Subject')
    date_joined = models.DateField(default=now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.employee_id} - {self.user.first_name} {self.user.last_name}"


class Class(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Grade 1", "Grade 2"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Section(models.Model):
    name = models.CharField(max_length=10)  # e.g., "A", "B", "C"
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class ClassSection(models.Model):
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True)
    academic_year = models.CharField(max_length=9)  # e.g., "2023-2024"
    room_number = models.CharField(max_length=10, blank=True)

    class Meta:
        unique_together = ['class_name', 'section', 'academic_year']

    def __str__(self):
        return f"{self.class_name} - {self.section} ({self.academic_year})"

class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True)
    credits = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.code})"

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    status_choices = [
        ('P', 'Present'),
        ('A', 'Absent'),
        ('L', 'Late'),
        ('E', 'Excused')
    ]
    status = models.CharField(max_length=1, choices=status_choices)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ['student', 'date']

    def __str__(self):
        return f"{self.student} - {self.date} - {self.get_status_display()}"

class Exam(models.Model):
    name = models.CharField(max_length=100)
    exam_type_choices = [
        ('MID', 'Mid Term'),
        ('FIN', 'Final Term'),
        ('UNIT', 'Unit Test'),
        ('QUIZ', 'Quiz')
    ]
    exam_type = models.CharField(max_length=4, choices=exam_type_choices)
    start_date = models.DateField()
    end_date = models.DateField()
    academic_year = models.CharField(max_length=9)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.academic_year}"

class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    max_marks = models.DecimalField(max_digits=5, decimal_places=2)
    remarks = models.TextField(blank=True)

    class Meta:
        unique_together = ['exam', 'student', 'subject']

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.exam}"

class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    fee_type_choices = [
        ('TUI', 'Tuition Fee'),
        ('LAB', 'Laboratory Fee'),
        ('TRA', 'Transportation Fee'),
        ('LIB', 'Library Fee'),
        ('OTH', 'Other Fee')
    ]
    fee_type = models.CharField(max_length=3, choices=fee_type_choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_date = models.DateField(null=True, blank=True)
    status_choices = [
        ('PEN', 'Pending'),
        ('PAI', 'Paid'),
        ('OVE', 'Overdue')
    ]
    status = models.CharField(max_length=3, choices=status_choices, default='PEN')
    payment_method = models.CharField(max_length=50, blank=True)
    receipt_number = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return f"{self.student} - {self.get_fee_type_display()} - {self.due_date}"