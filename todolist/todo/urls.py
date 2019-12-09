from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('signin/',views.login),
    path('register/',views.register.as_view()),
    path('afterlogin/',views.afterlogin),
    path('addtask/',views.addtask.as_view()),
    path('mytasks/',views.mytasks),
    path('deltask/<var>/',views.deltask),
    path('logout/',views.logout),
]