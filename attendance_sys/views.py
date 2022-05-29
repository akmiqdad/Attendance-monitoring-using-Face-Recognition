from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse


from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import get_user_model

from .forms import *
from .models import Student, Attendence
from .filters import AttendenceFilter

# from django.views.decorators import gzip

from .recognizer import Recognizer
from datetime import date


# User = get_user_model()

# @login_required
# def index(request):
#     if request.user.is_faculty:
#         return render(request, 'attendance_sys/facultyForm.html')
#     if request.user.is_student:
#         return render(request, 'attendance_sys/studentForm.html')
#     return render(request, 'info/logout.html')

@login_required(login_url='login')
def home(request):
    studentForm = CreateStudentForm()

    if request.method == 'POST':
        studentForm = CreateStudentForm(data=request.POST, files=request.FILES)
        # print(request.POST)
        stat = False
        try:
            student = Student.objects.get(registration_id=request.POST['registration_id'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get(
                'firstname') + " " + studentForm.cleaned_data.get('lastname')
            messages.success(request, 'Student ' + name +
                             ' was successfully added.')
            return redirect('home')
        else:
            messages.error(request, 'Student with Registration Id ' +
                           request.POST['registration_id']+' already exists.')
            return redirect('home')

    context = {'studentForm': studentForm}
    return render(request, 'attendance_sys/home.html', context)


def indexPage(request):

    return render(request, 'attendance_sys/index.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('account')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'attendance_sys/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    return redirect('index')


@login_required(login_url='login')
def updateStudentRedirect(request):
    context = {}
    if request.method == 'POST':
        try:
            reg_id = request.POST['reg_id']
            branch = request.POST['branch']
            student = Student.objects.get(
                registration_id=reg_id, branch=branch)
            updateStudentForm = CreateStudentForm(instance=student)
            context = {'form': updateStudentForm,
                       'prev_reg_id': reg_id, 'student': student}
        except:
            messages.error(request, 'Student Not Found')
            return redirect('home')
    return render(request, 'attendance_sys/student_update.html', context)


@login_required(login_url='login')
def updateStudent(request):
    if request.method == 'POST':
        context = {}
        try:
            student = Student.objects.get(
                registration_id=request.POST['prev_reg_id'])
            updateStudentForm = CreateStudentForm(
                data=request.POST, files=request.FILES, instance=student)
            if updateStudentForm.is_valid():
                updateStudentForm.save()
                messages.success(request, 'Updation Success')
                return redirect('home')
        except:
            messages.error(request, 'Updation Unsucessfull')
            return redirect('home')
    return render(request, 'attendance_sys/studentForm.html', context)


@login_required(login_url='login')
def takeAttendance(request):
    if request.method == 'POST':
        details = {
            'branch': request.POST['branch'],
            'year': request.POST['year'],
            'division': request.POST['division'],
            'period': request.POST['period'],
            'faculty': request.user.faculty
        }
        if Attendence.objects.filter(date=str(date.today()), branch=details['branch'], year=details['year'], division=details['division'], period=details['period']).count() != 0:
            messages.error(request, "Attendence already recorded.")
            return redirect('home')
        else:
            students = Student.objects.filter(
                branch=details['branch'], year=details['year'], division=details['division'])
            names = Recognizer(details)
            for student in students:
                if str(student.registration_id) in names:
                    attendence = Attendence(Faculty_Name=request.user.faculty,
                                            Student_ID=str(
                                                student.registration_id),
                                            period=details['period'],
                                            branch=details['branch'],
                                            year=details['year'],
                                            division=details['division'],
                                            status='Present')
                    attendence.save()
                else:
                    attendence = Attendence(Faculty_Name=request.user.faculty,
                                            Student_ID=str(
                                                student.registration_id),
                                            period=details['period'],
                                            branch=details['branch'],
                                            year=details['year'],
                                            division=details['division'])
                    attendence.save()
            attendences = Attendence.objects.filter(date=str(date.today(
            )), branch=details['branch'], year=details['year'], division=details['division'], period=details['period'])
            context = {"attendences": attendences, "ta": True}
            messages.success(request, "Attendence taking Success")
            return render(request, 'attendance_sys/attendence.html', context)
    context = {}
    return render(request, 'attendance_sys/home.html', context)


def searchAttendance(request):
    attendences = Attendence.objects.all()
    myFilter = AttendenceFilter(request.GET, queryset=attendences)
    attendences = myFilter.qs
    context = {'myFilter': myFilter, 'attendences': attendences, 'ta': False}
    return render(request, 'attendance_sys/attendence.html', context)


def facultyProfile(request):
    faculty = request.user.faculty
    form = FacultyForm(instance=faculty)
    context = {'form': form}
    return render(request, 'attendance_sys/facultyForm.html', context)


# class VideoCamera(object):
#     def __init__(self):
#         self.video = cv2.VideoCapture(0)
#     def __del__(self):
#         self.video.release()

#     def get_frame(self):
#         ret,image = self.video.read()
#         ret,jpeg = cv2.imencode('.jpg',image)
#         return jpeg.tobytes()


# def gen(camera):
#     while True:
#         frame = camera.get_frame()
#         yield(b'--frame\r\n'
#         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


# @gzip.gzip_page
# def videoFeed(request):
#     try:
#         return StreamingHttpResponse(gen(VideoCamera()),content_type="multipart/x-mixed-replace;boundary=frame")
#     except:
#         print("aborted")

# def getVideo(request):
#     return render(request, 'attendance_sys/videoFeed.html')


# @login_required()
# def add_student(request):
#     # If the user is not admin, they will be redirected to home
#     # if not request.user.is_superuser:
#     #     return redirect("/")

#     if request.method == 'POST':
#         # Retrieving all the form data that has been inputted
#         registration_id = request.POST['registration_id']
#         firstname = request.POST['firstname']
#         lastname = request.POST['lastname']
#         branch = request.POST['branch']
#         year = request.POST['year']
#         division = request.POST['division']
#         profile_pic = request.FILES['profile_pic']

#         user = User.objects.create_user(
#             username=registration_id,
#             password=registration_id
#         )
#         user.save()

#         # Creating a new student instance with given data and saving it.
#         Student(
#             user=user,
#             registration_id=registration_id,
#             firstname=firstname,
#             lastname=lastname,
#             branch=branch,
#             year=year,
#             division=division,
#             profile_pic=profile_pic,
#         ).save()
#         return redirect('/home')
#     context = {}
#     return render(request, 'attendance_sys/add_student.html', context)
