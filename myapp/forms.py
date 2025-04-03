from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('username', 'email', 'password1','password2')



from django import forms
from .models import AdminTimeSlot

class AdminTimeSlotForm(forms.ModelForm):
    class Meta:
        model = AdminTimeSlot
        fields = ['date', 'start_time', 'end_time', 'title', 'is_booked']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),  # Use HTML5 date picker
            'start_time': forms.TimeInput(attrs={'type': 'time'}),  # Use HTML5 time picker
            'end_time': forms.TimeInput(attrs={'type': 'time'})  # Use HTML5 time picker
        }

    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get("date")
        if date:
            # Set day_of_week based on date
            cleaned_data['day_of_week'] = date.strftime('%A')
        return cleaned_data


from django import forms
from .models import Appointment, AdminTimeSlot


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['admin', 'appointment_date', 'start_time', 'end_time', 'purpose']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].widget = forms.TimeInput(format='%H:%M', attrs={'type': 'time'})
        self.fields['end_time'].widget = forms.TimeInput(format='%H:%M', attrs={'type': 'time'})
        self.fields['appointment_date'].widget = forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})

        if 'admin' in self.data:
            try:
                admin_id = int(self.data.get('admin'))
                self.fields['start_time'].queryset = AdminTimeSlot.objects.filter(admin_id=admin_id, is_booked=False)
            except (ValueError, TypeError):
                pass
#ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
from django import forms
from .models import Meeting

class MeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ['title', 'date', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

#cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
