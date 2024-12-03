from django.contrib import admin
from .models import (
    User, Parent, Student, Teacher, StudentGroup,
    SchoolSubject, Grade, GradeColumn, Attendance,
    Meeting, ConsentTemplate, ParentConsent, ScheduledMeeting,
    CategoryStudentGroup, CategoryGradeValue, CategoryAttendanceStatus
)
from django.contrib.auth.models import Group

admin.site.register(User)
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
admin.site.register(CategoryStudentGroup)
admin.site.register(CategoryGradeValue)
admin.site.register(CategoryAttendanceStatus)