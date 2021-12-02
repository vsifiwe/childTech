from django.urls import path
from .views import (AppointmentDetail, AppointmentView, CourseDetail, CourseList, EnrollDetail, EnrollView, EventDetail, EventView, LessonDetail, LessonView, ProgramList, ProgramView,
                    RegisterAPI, UsersList, UserView)


# app_name = 'app'
urlpatterns = [
    path('register', RegisterAPI.as_view(), name="register"),
    path('users/', UsersList.as_view(), name='user'),
    path('users/<int:pk>/', UserView.as_view(), name='user-detail'),
    path('programs/', ProgramList.as_view(), name='programs-list'),
    path('programs/<int:pk>/', ProgramView.as_view(), name='program-detail'),
    path('courses/', CourseList.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseDetail.as_view(), name='course-detail'),
    path('lesson/', LessonView.as_view(), name='lessons'),
    path('lesson/<int:pk>/', LessonDetail.as_view(), name='lesson-detail'),
    path('enroll/', EnrollView.as_view(), name='enroll'),
    path('enroll/<int:pk>/', EnrollDetail.as_view(), name='enroll-detail'),
    path('appointment/', AppointmentView.as_view(), name='appointments'),
    path('appointment/<int:pk>/', AppointmentDetail.as_view(), name='app-detail'),
    path('events/', EventView.as_view(), name='events'),
    path('events/<int:pk>/', EventDetail.as_view(), name='event-detail'),
]
