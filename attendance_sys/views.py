from django.shortcuts import render, redirect

from django.views.generic.edit import CreateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import *
from .models import Student, Attendence
from .filters import AttendenceFilter,StudentAttendenceFilter


from .recognizer import Recognizer
from .chatbot import get_bot_response
from datetime import date
# from ..recScheduler.controller import control


User = get_user_model()


def indexPage(request):

    return render(request, 'attendance_sys/index.html')


def facultyLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('facultyhome')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'attendance_sys/facultylogin.html', context)


def studentLogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('studenthome')
        else:
            messages.info(request, 'Username or Password is incorrect')

    context = {}
    return render(request, 'attendance_sys/studentlogin.html', context)


@login_required(login_url='facultylogin')
def logoutUser(request):
    logout(request)
    return redirect('index')


@login_required(login_url='studentlogin')
def logoutUser(request):
    logout(request)
    return redirect('index')


@login_required(login_url='facultylogin')
def facultyHome(request):
    studentForm = CreateStudentForm()

    if request.method == 'POST':
        studentForm = CreateStudentForm(data=request.POST, files=request.FILES)
        # print(request.POST)
        stat = False
        try:
            student = Student.objects.get(
                registration_id=request.POST['registration_id'])
            stat = True
        except:
            stat = False
        if studentForm.is_valid() and (stat == False):
            studentForm.save()
            name = studentForm.cleaned_data.get(
                'first_name') + " " + studentForm.cleaned_data.get('last_name')
            messages.success(request, 'Student ' + name +
                             ' was successfully added.')
            return redirect('facultyhome')
        else:
            messages.error(request, 'Student with Registration Id ' +
                           request.POST['registration_id']+' already exists.')
            return redirect('facultyhome')

    context = {'studentForm': studentForm}
    return render(request, 'attendance_sys/facultyhome.html', context)


@login_required()
def chatBot(request):
    msg= request.POST['msg']
    get_bot_response(msg)
    return render(request, 'attendance_sys/chatbot.html',{'msg':msg})

@login_required(login_url='studentlogin')
def studentHome(request):
    return render(request, 'attendance_sys/studenthome.html')

@login_required(login_url = 'facultylogin')
def updateStudentRedirect(request):
    context = {}
    if request.method == 'POST':
        try:
            reg_id = request.POST['reg_id']
            branch = request.POST['branch']
            student = Student.objects.get(registration_id = reg_id, branch = branch)
            updateStudentForm = CreateStudentForm(instance=student)
            context = {'form':updateStudentForm, 'prev_reg_id':reg_id, 'student':student}
        except:
            messages.error(request, 'Student Not Found')
            return redirect('facultyhome')
    return render(request, 'attendance_sys/studentform.html', context)


@login_required(login_url='facultylogin')
def studentForm(request):
    if request.method == 'POST':
        context = {}
        try:
            student = Student.objects.get(registration_id = request.POST['prev_reg_id'])
            updateStudentForm = CreateStudentForm(data = request.POST, files=request.FILES, instance = student)
            if updateStudentForm.is_valid():
                updateStudentForm.save()
                messages.success(request, 'Updation Success')
                return redirect('home')
        except:
            messages.error(request, 'Updation Unsucessfull')
            return redirect('facultyhome')
    return render(request, 'attendance_sys/studentForm.html', context)



@login_required(login_url='studentlogin')
def studentProfile(request):
    student = request.user.student
    form = StudentForm(instance=student)
    context = {'form': form}
    return render(request, 'attendance_sys/studentprofile.html', context)


def testAttendance(request):
    if request.method == 'POST':
        details = {
            'subject': request.POST['subject'],
            'branch': request.POST['branch'],
            'year': request.POST['year'],
            'division': request.POST['division'],
            'period': request.POST['period']
        }
        if Attendence.objects.filter(date=str(date.today()), branch=details['branch'], year=details['year'], division=details['division'], period=details['period']).count() != 0:
            messages.error(request, "Attendence already recorded.")
            return redirect('facultyhome')
        else:
            students = Student.objects.filter(
                branch=details['branch'], year=details['year'], division=details['division'])
            names = Recognizer(details)
            for student in students:
                if str(student.registration_id) in names:
                    attendence = Attendence(Student_ID=str(
                        student.registration_id),
                        subject=details['subject'],
                        period=details['period'],
                        branch=details['branch'],
                        year=details['year'],
                        division=details['division'],
                        status='Present')
                    attendence.save()
                else:
                    attendence = Attendence(Student_ID=str(
                                                student.registration_id),
                                            subject=details['subject'],
                                            period=details['period'],
                                            branch=details['branch'],
                                            year=details['year'],
                                            division=details['division'])
                    attendence.save()
            attendences = Attendence.objects.filter(date=str(date.today(
            )), subject=details['subject'], branch=details['branch'], year=details['year'], division=details['division'], period=details['period'])
            context = {"attendences": attendences, "ta": True}
            messages.success(request, "Attendence taking Success")
            return render(request, 'attendance_sys/facultyattendance.html', context)
    context = {}
    return render(request, 'attendance_sys/home.html', context)

@login_required(login_url="/facultylogin")
def facultyAttendance(request):
    attendences = Attendence.objects.all()
    myFilter = AttendenceFilter(request.GET, queryset=attendences)
    attendences = myFilter.qs
    context = {'myFilter': myFilter, 'attendences': attendences, 'ta': False}
    return render(request, 'attendance_sys/facultyattendance.html', context)

@login_required(login_url="/studentlogin")
def studentAttendance(request):
    attendences = Attendence.objects.filter(Student_ID=request.user.username)
    myFilter = StudentAttendenceFilter(request.GET, queryset=attendences)
    attendences = myFilter.qs
    context = {'myFilter': myFilter, 'attendences': attendences, 'ta': False}
    return render(request, 'attendance_sys/studentattendance.html',context)

@login_required(login_url="/facultylogin")
def facultyProfile(request):
    faculty = request.user.faculty
    form = FacultyForm(instance=faculty)
    context = {'form': form}
    return render(request, 'attendance_sys/facultyform.html', context)


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


class add_student(LoginRequiredMixin,CreateView):
    login_url = '/facultylogin'
    model = User
    form_class = AddStudentForm
    template_name = 'attendance_sys/addstudent.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/studenthome')
