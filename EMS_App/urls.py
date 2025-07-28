from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.loginpw,name='login'),
    path('logout',views.logout_page,name='logout'),
    path('register',views.register,name='register'),
    path('addevent',views.addevent,name='addevent'),
    path('updateevent/<str:id>',views.loadevent,name='updateevent'),
    path('eventupdate/<str:id>',views.eventupdate,name='eventupdate'),
    path('deleteevent/<str:id>',views.deleteevent,name='deleteevent'),
    path('search',views.search,name='search'),

]
