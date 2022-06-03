from __future__ import division
from django.db import models

from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_faculty = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)


def user_directory_path(instance, filename):
    name, ext = filename.split(".")
    name = instance.user.first_name + instance.user.last_name
    filename = name + '.' + ext
    return 'Faculty_Images/{}'.format(filename)


class Faculty(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    # firstname = models.CharField(max_length=100, null=True, blank=True)
    # lastname = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    profile_pic = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return str(self.user.first_name + " " + self.user.last_name)


def student_directory_path(instance, filename):
    name, ext = filename.split(".")
    # + "_" + instance.branch + "_" + instance.year + "_" + instance.division
    name = instance.registration_id
    filename = name + '.' + ext
    return 'Student_Images/{}/{}/{}/{}'.format(instance.branch, instance.year, instance.division, filename)


class Student(models.Model):

    BRANCH = (
        ('CSE', 'CSE'),
        ('IT', 'IT'),
        ('ECE', 'ECE'),
        ('CIVIL', 'CIVIL'),
        ('MECH', 'MECH'),
        ('EEE', 'EEE'),
    )
    YEAR = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
    )
    DIVISION = (
        ('A', 'A'),
        ('B', 'B'),
    )
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    # firstname = models.CharField(max_length=100, null=True, blank=True)
    # lastname = models.CharField(max_length=100, null=True, blank=True)
    registration_id = models.CharField(max_length=100, null=True)
    # registration_id = models.OneToOneField(User, null = True, on_delete= models.CASCADE)
    branch = models.CharField(max_length=100, null=True, choices=BRANCH)
    year = models.CharField(max_length=100, null=True, choices=YEAR)
    division = models.CharField(max_length=100, null=True, choices=DIVISION)
    profile_pic = models.ImageField(
        upload_to=student_directory_path, null=True, blank=True)

    REQUIRED_FIELDS = ['registration_id', 'first_name', 'last_name']

    def __str__(self):
        return str(self.registration_id)


class Attendence(models.Model):
    # faculty = models.ForeignKey(Faculty, null = True, on_delete= models.SET_NULL)
    # student = models.ForeignKey(Student, null = True, on_delete= models.SET_NULL)
    # Faculty_Name = models.CharField(max_length=100, null=True, blank=True)
    Student_ID = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True)
    time = models.TimeField(auto_now_add=True, null=True)
    branch = models.CharField(max_length=100, null=True)
    year = models.CharField(max_length=100, null=True)
    division = models.CharField(max_length=100, null=True)
    period = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=100, null=True, default='Absent')

    def __str__(self):
        return str(self.Student_ID + "_" + str(self.date) + "_" + str(self.period))
