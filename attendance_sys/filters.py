from webbrowser import get
import django_filters
from numpy import greater

from .models import Attendence

class AttendenceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendence
        fields = '__all__'
        exclude = ['time','period','status']

class StudentAttendenceFilter(django_filters.FilterSet):
    class Meta:
        model = Attendence
        fields = ['subject','date','status']