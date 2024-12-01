"""
URL configuration for usos_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from .usos_api.views import (
    StudentViewSet, TeacherViewSet, ParentViewSet, GradeViewSet,
    CurrentUserView, UserInfoView,  GradeColumnView,
    GradeListCreateView, GradeDetailView, ScheduleView, 
    ConsentTemplateView, FeedView
)


"""from .usos_api.views import (
    UserViewSet, GroupViewSet, UserView, StudentGroupViewSet, GradeViewSet, GradeColumnViewSet, 
    ScheduledMeetingViewSet, ParentConsentViewSet, ConsentTemplateViewSet
)
"""
router = routers.DefaultRouter()
"""router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)"""

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
"""urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]"""



"""router.register(r'student-groups', StudentGroupViewSet, basename='studentgroup')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'grade-columns', GradeColumnViewSet, basename='gradecolumn')
router.register(r'meetings', ScheduledMeetingViewSet, basename='meeting')
router.register(r'econsent', ParentConsentViewSet, basename='parentconsent')
router.register(r'econsent-templates', ConsentTemplateViewSet, basename='consenttemplate')

urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('user/<int:pk>/', UserViewSet.as_view(), name='user-detail'),
    path('', include(router.urls)),
]"""



router.register('students', StudentViewSet, basename='student')
router.register('teachers', TeacherViewSet, basename='teacher')
router.register('parents', ParentViewSet, basename='parent')
router.register('grades', GradeViewSet, basename='grade')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('user/', CurrentUserView.as_view(), name='current_user'),
    path('user/<int:user_id>/info/', UserInfoView.as_view(), name='user_info'),
    path('grades/columns/<int:subject_id>/', GradeColumnView.as_view(), name='grade_columns'),
    path('grades/<int:user_id>/<int:subject_id>/', GradeListCreateView.as_view(), name='user_subject_grades'),
    path('grades/<int:grade_id>/', GradeDetailView.as_view(), name='grade_detail'),
    path('meetings/schedule/', ScheduleView.as_view(), name='schedule'),
    path('econsent/templates/<int:template_consent_id>/', ConsentTemplateView.as_view(), name='consent_template_detail'),
    path('feed/<int:user_id>/', FeedView.as_view(), name='user_feed'),
]

