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
    path("demo/", demo, name="demo"),
    path("", login_page, name="login_page"),
    path("admin_home/", admin_home, name="admin_home"),
    path("student_home/", student_home, name="student_home"),
    path("teacher_home/", teacher_home, name="teacher_home"),
    path("admin_view_profile/", admin_view_profile, name="admin_view_profile"),
    path("view_users/", view_users, name="view_users"),
    path("register_user/", register_user, name="register_user"),
    path("update_user/<id>", update_user, name="update_user"),
    path("delete_user/<id>", deleteuser, name="delete_user"),
    path("logout/", logout_page, name="logout"),
    path("view_courses/", view_courses, name="view_courses"),
    path("register_course/", register_course, name="register_course"),
    path("delete_course/<id>", deletecourse, name="delete_course"),
    path("update_course/<id>", updatecourse, name="update_course"),
    path("register_hall/", registerhall, name="register_hall"),
    path("delete_hall/<id>", deletehall, name="delete_hall"),
    path("edit_hall_layout/<name>", edithalllayout, name="edit_hall_layout"),
    # path("update_hall/<id>", updatehall, name="update_hall"),
    path(
        "remove_seat_from_hall/<id>", removeseatfromhall, name="remove_seat_from_hall"
    ),
    path("add_seat_to_hall/<id>", addseattohall, name="add_seat_to_hall"),
    path(
        "add_columnspace_to_hall/<id>",
        addcolumnspacetohall,
        name="add_columnspace_to_hall",
    ),
    path(
        "remove_columnspace_from_hall/<id>",
        removecolumnspacefromhall,
        name="remove_columnspace_from_hall",
    ),
    path(
        "add_rowspace_to_hall/<id>",
        addrowspacetohall,
        name="add_rowspace_to_hall",
    ),
    path(
        "remove_rowspace_from_hall/<id>",
        removerowspacefromhall,
        name="remove_rowspace_from_hall",
    ),
    path("view_hall_layout/<id>", viewhalllayout, name="view_hall_layout"),
    path("view_hall_layout/<id>", viewhalllayout, name="view_hall_layout"),
    path("admin_events_view/", admin_events_view, name="admin_events_view"),
    path("create_new_event/", create_new_event, name="create_new_event"),
    path("delete_event/<id>", delete_event, name="delete_event"),
    path(
        "create_new_event_courses/<id>",
        create_new_event_courses,
        name="create_new_event_courses",
    ),
    path(
        "create_new_event_halls/<id>",
        create_new_event_halls,
        name="create_new_event_halls",
    ),
    path(
        "admin_view_event_info/<id>",
        admin_view_event_info,
        name="admin_view_event_info",
    ),
    path("seed_courses/", seed_courses, name="seed_courses"),
    path("seed_students/", seed_students, name="seed_students"),
    path(
        "show_student_allocation_info/<id>",
        show_student_allocation_info,
        name="show_student_allocation_info",
    ),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
