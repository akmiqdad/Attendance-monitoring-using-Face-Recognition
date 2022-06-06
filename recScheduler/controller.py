# from datetime import datetime, date
# from operator import indexOf
# from ..attendance_sys.models import *
# from ..attendance_sys.forms import *
# from ..attendance_sys.models import Student, Attendence
# from ..attendance_sys.filters import AttendenceFilter
# from ..attendance_sys.recognizer import Recognizer


# def timeDetails():



# def assignDetails():
#     camdetails=[('CSE',4,'A'),('CSE',4,'B'),('IT',4,'A'),('IT',4,'B')]
#     for details in camdetails:
#         branch=details[0]
#         year=details[1]
#         section=details[2]
#         ind=indexOf(details)
#         return branch,year,section,ind

# def takeAttendance(details,ind):
#     assignDetails()
#     try:
#         if Attendence.objects.filter(date=str(date.today()),details.branch,details.year,details.section,period).count() != 0):
#             exit
#     except:
#         students = Student.objects.filter(
#             branch=details['branch'], year=details['year'], section=details['section'])
#         names = Recognizer(details,ind)
#         for student in students:
#                 if str(student.registration_id) in names:
#                     attendence = Attendence( Student_ID=str(student.registration_id),
#                     period=details['period'],
#                     branch=details['branch'],
#                     year=details['year'],
#                     section=details['section'],
#                     status='Present')
#                     attendence.save()
#                 else:
#                     attendence = Attendence(                    Student_ID=str(student.registration_id),
#                     period=details['period'],
#                     branch=details['branch'],
#                     year=details['year'],
#                     section=details['section'])
#                     attendence.save()