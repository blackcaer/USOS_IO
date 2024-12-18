from usos_backend.usos_api.models import ScheduledMeeting


def get_scheduled_meetings(user, start_of_week, end_of_week):
    if user.role == 'student':
        print('searching student')
        scheduled_meetings = ScheduledMeeting.objects.filter(
            school_subject__student_group__students=user.related_student)

    elif user.role == 'teacher':
        scheduled_meetings = ScheduledMeeting.objects.filter(
            teacher=user.related_teacher)
    elif user.role == 'parent':
        print('searching parent')

        scheduled_meetings = ScheduledMeeting.objects.filter(
            school_subject__student_group__students=user.related_parent.children.first()
        )

    return scheduled_meetings
