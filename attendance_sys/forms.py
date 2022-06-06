from importlib.abc import ExecutionLoader
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.db import transaction
from .models import *

class AddStudentForm(UserCreationForm):
    is_student = True
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    registation_id = forms.CharField(required=True)
    branch = forms.CharField(required=True)
    year = forms.CharField(required=True)
    division = forms.CharField(required=True)
    profile_pic = forms.FileField(required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username','first_name','last_name','registation_id','branch','year','division','profile_pic']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.registation_id=self.cleaned_data.get('registation_id')
        student.branch=self.cleaned_data.get('branch')
        student.year=self.cleaned_data.get('year')
        student.division=self.cleaned_data.get('division')
        student.profile_pic=self.cleaned_data.get('profile_pic')
        student.save()
        return user


# class FacultyForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)

#     class Meta(UserCreationForm.Meta):
#         model = User
    
#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_faculty = True
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         user.save()
#         faculty = Faculty.objects.create(user=user)
#         faculty.phone=self.cleaned_data.get('phone')
#         faculty.email=self.cleaned_data.get('email')
#         faculty.profile_pic=self.cleaned_data.get('profile_pic')
#         faculty.save()
#         return user


class CreateStudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(CreateStudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
class FacultyForm(ModelForm):
    class Meta:
        model = Faculty
        fields = '__all__'
        exclude = ['user']
    def __init__(self, *args, **kwargs):
        super(FacultyForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'    


class StudentForm(ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        exclude = ['user']
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'  