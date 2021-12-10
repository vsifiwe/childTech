from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import (
    ParentAppointmentSerializer, SchoolAppointmentSerializer, CourseSerializer, EnrollSerializer, EventSerializer, LessonFalseSerializer, LessonSerializer, UsersSerializer, RegisterSerializer, UserSerializer, ProgramSerializer)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import (Course, Enroll, Event, Lesson,
                     ParentAppointment, Program, SchoolAppointment)
from .permissions import (ReadOnly)
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import MyTokenObtainPairSerializer


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "user": UsersSerializer(user, context=self.get_serializer_context()).data,
        })


class UsersList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UsersSerializer
    permission_classes = [IsAdminUser]


class UserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProgramList(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class ProgramView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class CourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class CourseDetail(APIView):
    def get_course(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        course = self.get_course(pk)
        serializer = CourseSerializer(course)
        all_lessons = course.lesson_set.all()
        clean_lessons = []
        for lesson in all_lessons:
            if lesson.preview == True:
                print(lesson)
                l = LessonSerializer(lesson)
                clean_lessons.append(l.data)
            else:
                l = LessonFalseSerializer(lesson)
                clean_lessons.append(l.data)

        data = {**serializer.data, 'lessons': clean_lessons}

        return Response(data)

    def put(self, request, pk, format=None):
        course = self.get_course(pk)
        serializer = CourseSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_course(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class LessonView(generics.ListCreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonFalseSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class LessonDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonFalseSerializer
    permission_classes = [IsAdminUser | ReadOnly]


@api_view(('POST',))
@permission_classes([IsAuthenticated])
def EnrollView(request, pk):
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    user, token = response
    course = Course.objects.get(id=pk)
    course_data = CourseSerializer(course).data
    print(course_data)
    try:
        Enroll.objects.get(course=pk, user=token.payload['user_id'])
        return Response({"message": "You are already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)
    except Enroll.DoesNotExist:
        data = {
            'course': pk,
            'user': token.payload['user_id']
        }
        serializer = EnrollSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnrollList(generics.ListAPIView):
    queryset = Enroll.objects.all()
    serializer_class = EnrollSerializer
    permission_classes = [IsAdminUser]


class EnrollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enroll.objects.all()
    serializer_class = EnrollSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class ParentAppointmentCreate(generics.CreateAPIView):
    queryset = ParentAppointment.objects.all()
    serializer_class = ParentAppointmentSerializer
    # permission_classes = [IsAuthenticated]


class ParentAppointmentView(generics.ListAPIView):
    queryset = ParentAppointment.objects.all()
    serializer_class = ParentAppointmentSerializer
    permission_classes = [IsAdminUser]


class ParentAppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = ParentAppointment.objects.all()
    serializer_class = ParentAppointmentSerializer
    permission_classes = [IsAdminUser]


class SchoolAppointmentCreate(generics.CreateAPIView):
    queryset = SchoolAppointment.objects.all()
    serializer_class = SchoolAppointmentSerializer
    # permission_classes = [IsAuthenticated]


class SchoolAppointmentView(generics.ListAPIView):
    queryset = SchoolAppointment.objects.all()
    serializer_class = SchoolAppointmentSerializer
    permission_classes = [IsAdminUser]


class SchoolAppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = SchoolAppointment.objects.all()
    serializer_class = SchoolAppointmentSerializer
    permission_classes = [IsAdminUser]


class EventView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser | ReadOnly]


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def LearnView(request, pk):
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    user, token = response

    try:
        enrollment = Enroll.objects.get(
            course=pk, user=token.payload['user_id'])
        lessons = Course.objects.get(id=pk).lesson_set.all()
        clean_lessons = LessonSerializer(lessons, many=True).data
        print(clean_lessons)
        return Response({"message": clean_lessons})
    except Enroll.DoesNotExist:
        return Response({"message": "not enrolled"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(('GET',))
@permission_classes([IsAuthenticated])
def PaidView(request):
    JWT_authenticator = JWTAuthentication()
    response = JWT_authenticator.authenticate(request)
    user, token = response

    try:
        enrolls = Enroll.objects.filter(user=token.payload['user_id'])
        enrollments = EnrollSerializer(enrolls, many=True).data
        courses = []
        for e in enrollments:
            c = Course.objects.get(id=e['course'])
            course = CourseSerializer(c).data
            courses.append(course)

        if not courses:
            return Response({"message": "You are not enrolled in any lesson"})

        return Response({"courses": courses})
    except Enroll.DoesNotExist:
        return Response({"message": "You are not enrolled in any lesson."})
