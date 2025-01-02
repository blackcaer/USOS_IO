from django.contrib import admin
from .models import (
    User, Parent, Student, Teacher, StudentGroup,
    SchoolSubject, Grade, GradeColumn, Attendance,
    Meeting, ConsentTemplate, ParentConsent, ScheduledMeeting,
    CategoryGradeValue, CategoryAttendanceStatus
)
from django.contrib.auth.models import Group
from .serializers import UserSerializer

class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'role']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'role']
    fields = ['username', 'password', 'first_name', 'last_name', 'email', 'status', 'birth_date', 'sex', 'phone_number', 'photo_url', 'role']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ['role']
        return []

    def save_model(self, request, obj, form, change):
        if not change:  # Only create related object if this is a new user
            serializer = UserSerializer(data=form.cleaned_data)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValueError("Invalid data: {}".format(serializer.errors))
        else:
            super().save_model(request, obj, form, change)

admin.site.register(User, UserAdmin)
admin.site.register(Parent)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(StudentGroup)
admin.site.register(SchoolSubject)
admin.site.register(Grade)
admin.site.register(GradeColumn)
admin.site.register(Attendance)
admin.site.register(Meeting)
admin.site.register(ConsentTemplate)
admin.site.register(ParentConsent)
admin.site.register(ScheduledMeeting)
#admin.site.register(CategoryStudentGroup)
admin.site.register(CategoryGradeValue)
admin.site.register(CategoryAttendanceStatus)