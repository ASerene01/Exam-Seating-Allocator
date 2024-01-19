"""
URL configuration for main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from api.views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", login_page, name="login_page"),
    path("admin_home/", admin_home, name="admin_home"),
    path("admin_view_profile/", admin_view_profile, name="admin_view_profile"),
    path("update_user/<id>", update_user, name="update_user"),
    path("delete_user/<id>", deleteuser, name="delete_user"),
    path("register/", register, name="register"),
    path("logout/", logout_page, name="logout"),
    path("register_course/", register_course, name="register_course"),
    path("delete_course/<id>", deletecourse, name="delete_course"),
    path("update_course/<id>", updatecourse, name="update_course"),
    path("register_hall/", registerhall, name="register_hall"),
    path("delete_hall/<id>", deletehall, name="delete_halll"),
    path("edit_hall_layout/<name>", edithalllayout, name="edit_hall_layout"),
    # path("update_hall/<id>", updatehall, name="update_hall"),
    path("student_home/", student_home, name="student_home"),
    path("teacher_home/", teacher_home, name="teacher_home"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
