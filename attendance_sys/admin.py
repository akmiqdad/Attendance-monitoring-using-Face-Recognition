from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (                      # new fieldset added on to the bottom
            'Custom Field Heading',  # group heading of your choice; set to None for a blank space instead of a header
            {
                'fields': (
                    'is_faculty',
                    'is_student'
                ),
            },
        ),
    )

admin.site.register(User,CustomUserAdmin)
admin.site.register(Faculty)
admin.site.register(Student)
admin.site.register(Attendence)