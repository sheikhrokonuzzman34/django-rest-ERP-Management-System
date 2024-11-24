# views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from datetime import datetime, timedelta
from django.db.models import Sum, Avg
from django.utils.timezone import now

from .models import (
    Student, Teacher, Class, Section, ClassSection, 
    Subject, Attendance, Exam, ExamResult, Fee
)
from .serializers import (
    StudentSerializer, TeacherSerializer, ClassSerializer, 
    SectionSerializer, ClassSectionSerializer, SubjectSerializer,
    AttendanceSerializer, ExamSerializer, ExamResultSerializer,
    FeeSerializer
)

# Student Management Views
@swagger_auto_schema(
    methods=['get'],
    responses={200: StudentSerializer(many=True)},
    operation_description="Get list of all students"
)
@swagger_auto_schema(
    methods=['post'],
    request_body=StudentSerializer,
    responses={201: StudentSerializer()},
    operation_description="Create a new student"
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def student_list(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=['get', 'put', 'delete'],
    responses={
        200: StudentSerializer(),
        204: 'No Content',
        404: 'Not Found'
    }
)
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def student_detail(request, pk):
    student = get_object_or_404(Student, pk=pk)

    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Teacher Management Views
@swagger_auto_schema(
    methods=['get', 'post'],
    responses={
        200: TeacherSerializer(many=True),
        201: TeacherSerializer()
    }
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def teacher_list(request):
    if request.method == 'GET':
        teachers = Teacher.objects.all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Class and Section Management Views
@swagger_auto_schema(
    methods=['get', 'post'],
    responses={
        200: ClassSectionSerializer(many=True),
        201: ClassSectionSerializer()
    }
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def class_section_list(request):
    if request.method == 'GET':
        class_sections = ClassSection.objects.all()
        serializer = ClassSectionSerializer(class_sections, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ClassSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Attendance Management Views
@swagger_auto_schema(
    method='post',
    request_body=AttendanceSerializer,
    responses={201: AttendanceSerializer()}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_attendance(request):
    serializer = AttendanceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('student_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('start_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
        openapi.Parameter('end_date', openapi.IN_QUERY, type=openapi.TYPE_STRING, format='date'),
    ],
    responses={200: AttendanceSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_attendance_report(request):
    student_id = request.query_params.get('student_id')
    start_date = request.query_params.get('start_date')
    end_date = request.query_params.get('end_date')
    
    attendance = Attendance.objects.all()
    if student_id:
        attendance = attendance.filter(student_id=student_id)
    if start_date:
        attendance = attendance.filter(date__gte=start_date)
    if end_date:
        attendance = attendance.filter(date__lte=end_date)
    
    serializer = AttendanceSerializer(attendance, many=True)
    return Response(serializer.data)

# Exam Management Views
@swagger_auto_schema(
    methods=['get', 'post'],
    responses={
        200: ExamSerializer(many=True),
        201: ExamSerializer()
    }
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def exam_management(request):
    if request.method == 'GET':
        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = ExamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=ExamResultSerializer,
    responses={201: ExamResultSerializer()}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_exam_result(request):
    serializer = ExamResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('student_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
        openapi.Parameter('exam_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER),
    ],
    responses={200: ExamResultSerializer(many=True)}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_exam_results(request):
    student_id = request.query_params.get('student_id')
    exam_id = request.query_params.get('exam_id')
    
    results = ExamResult.objects.all()
    if student_id:
        results = results.filter(student_id=student_id)
    if exam_id:
        results = results.filter(exam_id=exam_id)
    
    serializer = ExamResultSerializer(results, many=True)
    return Response(serializer.data)

# Fee Management Views
@swagger_auto_schema(
    methods=['get', 'post'],
    responses={
        200: FeeSerializer(many=True),
        201: FeeSerializer()
    }
)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def fee_management(request):
    if request.method == 'GET':
        fees = Fee.objects.all()
        serializer = FeeSerializer(fees, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = FeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'fee_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'payment_method': openapi.Schema(type=openapi.TYPE_STRING),
            'paid_amount': openapi.Schema(type=openapi.TYPE_NUMBER),
        }
    ),
    responses={200: FeeSerializer()}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def record_fee_payment(request):
    fee_id = request.data.get('fee_id')
    fee = get_object_or_404(Fee, pk=fee_id)
    
    fee.paid_date = now()
    fee.payment_method = request.data.get('payment_method')
    fee.status = 'PAI'
    fee.save()
    
    serializer = FeeSerializer(fee)
    return Response(serializer.data)

# Dashboard Views
@swagger_auto_schema(
    method='get',
    responses={200: openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'total_students': openapi.Schema(type=openapi.TYPE_INTEGER),
            'total_teachers': openapi.Schema(type=openapi.TYPE_INTEGER),
            'recent_attendance': AttendanceSerializer(many=True),
            'upcoming_exams': ExamSerializer(many=True),
            'pending_fees': FeeSerializer(many=True),
        }
    )}
)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    today = now().date()
    
    summary = {
        'total_students': Student.objects.count(),
        'total_teachers': Teacher.objects.count(),
        'recent_attendance': AttendanceSerializer(
            Attendance.objects.filter(date=today),
            many=True
        ).data,
        'upcoming_exams': ExamSerializer(
            Exam.objects.filter(start_date__gte=today),
            many=True
        ).data,
        'pending_fees': FeeSerializer(
            Fee.objects.filter(status='PEN'),
            many=True
        ).data,
    }
    
    return Response(summary)