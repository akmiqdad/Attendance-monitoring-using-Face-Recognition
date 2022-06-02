from django.urls import path

from . import views


urlpatterns = [
    path('', views.indexPage, name = 'index'),
    path('facultyhome/', views.facultyHome, name = 'facultyhome'),
    path('studenthome/', views.studentHome, name = 'studenthome'),
    path('facultylogin/', views.facultyLogin, name='facultylogin'),
    path('studentlogin/', views.studentLogin, name='studentlogin'),
    path('logout/', views.logoutUser, name='logout'),
    path('faculty_attendance/', views.facultyAttendance, name='facultyattendance'),
    path('student_attendance/', views.studentAttendance, name='studentattendance'),
    path('account/', views.facultyProfile, name='facultyform'),

    path('updateStudentRedirect/', views.updateStudentRedirect, name='updateStudentRedirect'),
    path('updateStudent/', views.updateStudent, name='updateStudent'),
    path('attendance/', views.takeAttendance, name='attendance'),
    path('addStudent/', views.add_student.as_view(), name='add_student'),
    # path('video_feed/', views.videoFeed, name='video_feed'),
    # path('videoFeed/', views.getVideo, name='videoFeed'),
]