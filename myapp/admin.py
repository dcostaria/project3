from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    model = User
    # Customize the admin interface here if needed

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
# Register your models here.


from django.contrib import admin
from .models import AdminTimeSlot, Appointment

@admin.register(AdminTimeSlot)
class AdminTimeSlotAdmin(admin.ModelAdmin):
    list_display = ('admin', 'day_of_week', 'date', 'start_time', 'end_time', 'title', 'is_booked')
    search_fields = ('admin__username', 'day_of_week', 'title')

from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'admin', 'appointment_date', 'start_time', 'end_time', 'purpose', 'status')

from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'timestamp', 'is_read']




from django.contrib import admin
from .models import Events

class EventsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'start', 'end', 'is_recurring', 'admin')


from django.contrib import admin
from .models import Meeting, Invitation

class MeetingAdmin(admin.ModelAdmin):
    list_display = ['title', 'date', 'start_time', 'end_time', 'created_by']  # Display these fields in the list view


class InvitationAdmin(admin.ModelAdmin):
    list_display = ['meeting', 'invitee', 'status', 'decline_reason']  # Display these fields in the list view


# Register the models with the admin panel
admin.site.register(Meeting, MeetingAdmin)
admin.site.register(Invitation, InvitationAdmin)
