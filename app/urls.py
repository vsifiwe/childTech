from django.urls import path
from .views import (AppointmentView, ContactView, ParentAppointmentCreate, ParentAppointmentDetail, SchoolAppointmentCreate, SchoolAppointmentDetail, CourseDetail, CourseList, EnrollDetail, EnrollList, EnrollView, EventDetail, EventView, LearnView, LessonDetail, LessonView, PaidView, ProgramList, ProgramView,
                    RegisterAPI, UsersList, UserView, dataView, Payment_response)


# app_name = 'app'
urlpatterns = [
    path('register', RegisterAPI.as_view(), name="register"),
    path('users/', UsersList.as_view(), name='user'),
    path('users/<int:pk>/', UserView.as_view(), name='user-detail'),
    path('programs/', ProgramList.as_view(), name='programs-list'),
    path('programs/<int:pk>/', ProgramView.as_view(), name='program-detail'),
    path('courses/', CourseList.as_view(), name='courses'),
    path('courses/<int:pk>/', CourseDetail.as_view(), name='course-detail'),
    path('courses/<int:pk>/learn', LearnView, name='course-learn'),
    path('courses/<int:pk>/enroll', EnrollView, name='enroll'),
    path('courses/paid', PaidView, name='paid'),
    path('lesson/', LessonView.as_view(), name='lessons'),
    path('lesson/<int:pk>/', LessonDetail.as_view(), name='lesson-detail'),
    path('enroll/all', EnrollList.as_view(), name='enroll-list'),
    path('enroll/<int:pk>/', EnrollDetail.as_view(), name='enroll-detail'),
    #     path('appointment/parent', ParentAppointmentView.as_view(), name='parent-list'),
    path('appointment/parent/create',
         ParentAppointmentCreate.as_view(), name='parent-create'),
    path('appointment/parent/<int:pk>/',
         ParentAppointmentDetail.as_view(), name='parent-detail'),
    #     path('appointment/school/', SchoolAppointmentView.as_view(), name='school-list'),
    path('appointment/school/create',
         SchoolAppointmentCreate.as_view(), name='school-create'),
    path('appointment/school/<int:pk>/',
         SchoolAppointmentDetail.as_view(), name='school-detail'),
    path('events/', EventView.as_view(), name='events'),
    path('events/<int:pk>/', EventDetail.as_view(), name='event-detail'),
    path('contact/', ContactView, name='contact-us'),
    path('data/', dataView, name='data'),
    path('appointment/', AppointmentView, name='app-list'),
    path('callback/', Payment_response, name='callback')
]
