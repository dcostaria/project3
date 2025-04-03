from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class AdminTimeSlot(models.Model):
    admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True})
    day_of_week = models.CharField(max_length=20)
    start_time = models.TimeField(null=True)  # Allow null values temporarily
    end_time = models.TimeField(null=True)  # Allow null values temporarily
    is_booked = models.BooleanField(default=False)
    date = models.DateField(default=timezone.now)  # Field for the date
    title = models.CharField(max_length=255, blank=True)  # Field for the title

    def save(self, *args, **kwargs):
        if self.date:
            self.day_of_week = self.date.strftime('%A')
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.admin.username} - {self.day_of_week} {self.date} {self.start_time} to {self.end_time} ({self.title})"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('P', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': False}, related_name='user_appointments')
    admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': True}, related_name='admin_appointments')
    appointment_date = models.DateField()
    start_time = models.TimeField(null=True)  # Allow null values temporarily
    end_time = models.TimeField(null=True)  # Allow null values temporarily
    purpose = models.CharField(max_length=255)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')

    def __str__(self):
        return f"Appointment by {self.user.username} with {self.admin.username} on {self.appointment_date} from {self.start_time} to {self.end_time}"


from django.utils import timezone

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='general_notifications')  # Changed related_name
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message}"


from django.db import models

from django.contrib.auth.models import User  # Import User model

class Events(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    start = models.DateTimeField(null=True, blank=True)
    end = models.DateTimeField(null=True, blank=True)
    is_recurring = models.BooleanField(default=False)  # Indicate if the event is recurring
    admin = models.ForeignKey(User, on_delete=models.CASCADE)  # Link event to an admin (user)

    class Meta:
        db_table = "tblevents"

#FFFFfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Meeting(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_meetings')

    def __str__(self):
        return self.title

class Invitation(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='invitations')
    invitee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invitations')
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    decline_reason = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.invitee.username} - {self.status} - {self.meeting.title}"


#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages')
    message = models.TextField()
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='messages')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message for {self.user.username} - {self.message}"