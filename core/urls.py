from django.conf.urls import url
from core import views

urlpatterns = [
    url(r'^search/$', views.student_search),
    url(r'^get_students_by_faculty/$', views.get_students_by_faculty),
    url(r'^students/(?P<name>\w+)-(?P<surname>\w+)', views.student_info, name="student-detail"),
    url(r'^$', views.index, name="home"),
    url(r'^get_specialization/$', views.get_specialization),
    url(r'^get_students/$', views.get_students),
    url(r'^add_rev/', views.add_rev),
]

