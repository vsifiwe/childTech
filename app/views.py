from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import (
    AppointmentSerializer, CourseSerializer, EnrollSerializer, EventSerializer, LessonFalseSerializer, LessonSerializer, UsersSerializer, RegisterSerializer, UserSerializer, ProgramSerializer)
from django.contrib.auth.models import User
from rest_framework.permissions import IsAdminUser
from .models import (Appointment, Course, Enroll, Event, Lesson, Program)
from .permissions import (ReadOnly)
from rest_framework.views import APIView
from django.http import Http404


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


class EnrollView(generics.ListCreateAPIView):
    queryset = Enroll.objects.all()
    serializer_class = EnrollSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class EnrollDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Enroll.objects.all()
    serializer_class = EnrollSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class AppointmentView(generics.ListCreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class AppointmentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class EventView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser | ReadOnly]


class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminUser | ReadOnly]
