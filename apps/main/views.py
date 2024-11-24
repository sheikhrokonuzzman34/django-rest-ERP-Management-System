# views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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

# Student Views
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
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(
    methods=['get'],
    responses={200: StudentSerializer()},
    operation_description="Get student details"
)
@swagger_auto_schema(
    methods=['put'],
    request_body=StudentSerializer,
    responses={200: StudentSerializer()},
    operation_description="Update student details"
)
@swagger_auto_schema(
    methods=['delete'],
    responses={204: 'No content'},
    operation_description="Delete student"
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

# Attendance Views
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'student_id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'status': openapi.Schema(type=openapi.TYPE_STRING, enum=['P', 'A', 'L', 'E']),
            'remarks': openapi.Schema(type=openapi.TYPE_STRING)
        }
    ),
    responses={201: AttendanceSerializer()},
    operation_description="Mark student attendance"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def mark_attendance(request):
    serializer = AttendanceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Exam Results Views
@swagger_auto_schema(
    method='post',
    request_body=ExamResultSerializer,
    responses={201: ExamResultSerializer()},
    operation_description="Add exam results"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_exam_result(request):
    serializer = ExamResultSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Fee Management Views
@swagger_auto_schema(
    method='post',
    request_body=FeeSerializer,
    responses={201: FeeSerializer()},
    operation_description="Add fee record"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_fee(request):
    serializer = FeeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


