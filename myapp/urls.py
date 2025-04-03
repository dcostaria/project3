from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('start/', views.start, name='start'),
    path('logout_confirm/', views.logout_confirm_view, name='logout_confirm'),
    path('logout/', views.logout_view, name='logout'),
    path('add-time-slot/', views.add_time_slot, name='add_time_slot'),
    path('time_slot_list/', views.time_slot_list, name='time_slot_list'),
    path('book_appointment/', views.book_appointment, name='book_appointment'),
    path('appointment_success/',views.appointment_success, name='appointment_success' ),
    path('manage_appointments/',views.manage_appointments, name='manage_appointments' ),
    path('notifications/',views.notifications, name='notifications' ),
    path('all_events/', views.all_events, name='all_events'),
    path('add_event/', views.add_event, name='add_event'),
    path('update/', views.update, name='update'),
    path('remove/',views.remove,name='remove'),
    path('index/', views.index, name='index'),
    path('add_recurring_event/', views.add_recurring_event, name='add_recurring_event'),
    path('create-meeting/', views.create_meeting, name='create_meeting'),

    path('messages/', views.view_messages, name='view_messages'),
    path('week/', views.week, name='week'),
    path('month/', views.month, name='month'),
    path('userhome/', views.userhome, name='userhome'),
    path('meeting-responses/', views.view_meeting_responses, name='meeting_status'),
   ]
