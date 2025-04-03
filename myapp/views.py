from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import  UserRegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.cache import cache_control
from django.shortcuts import get_object_or_404

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            # Ensure the user is registered as a regular user (not admin)
            user.is_staff = False
            user.save()
            messages.success(request, f'Account created for {user.username}')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register_view.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Check if the user is staff
            if user.is_staff:
                return redirect('month')  # Redirect to 'month' page if the user is staff
            else:
                return redirect('home')  # Redirect to 'home' page if the user is not staff
        else:
            messages.info(request, 'Username OR password is incorrect')

    return render(request, 'login_view.html')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    if request.user.is_staff:
        greeting = "Hello Admin"
    else:
        greeting = "Hello User"


    context = {'greeting': greeting}
    return render(request, 'home.html', context)

def start(request):
    return render(request, 'start.html')

def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def logout_confirm_view(request):
    if request.method == 'GET':
        confirm = request.GET.get('confirm')
        if confirm == 'yes':
            logout(request)
            return redirect('login')
    return render(request, 'logout_confirm.html')


from django.shortcuts import render, redirect
from .models import AdminTimeSlot, Appointment, Notification

from .forms import AdminTimeSlotForm
from .forms import AppointmentForm

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import AdminTimeSlotForm


@login_required
def add_time_slot(request):
    if request.method == 'POST':
        form = AdminTimeSlotForm(request.POST)
        if form.is_valid():
            time_slot = form.save(commit=False)
            time_slot.admin = request.user
            time_slot.save()
            return redirect('time_slot_list')  # Redirect to time slot list view
    else:
        form = AdminTimeSlotForm()

    return render(request, 'add_time_slot.html', {'form': form})


def time_slot_list(request):
    time_slots = AdminTimeSlot.objects.filter(admin=request.user)
    return render(request, 'time_slot_list.html', {'time_slots': time_slots})


from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import AppointmentForm
from .models import AdminTimeSlot, Appointment

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user  # Assign the logged-in user to the appointment

            # Check if the admin has scheduled any time slots for the given date
            booked_time_slots = AdminTimeSlot.objects.filter(
                admin=appointment.admin,
                date=appointment.appointment_date,
                start_time__lte=appointment.start_time,
                end_time__gte=appointment.end_time,
                is_booked=True
            )

            if booked_time_slots.exists():
                # Time slot is already booked
                messages.error(request, 'The selected time slot is not available. Please try again.')
                return redirect('book_appointment')

            # If no booked time slots conflict, proceed to book the appointment
            appointment.status = 'P'  # Set status to Pending
            appointment.save()

            # Mark the time slot as booked
            AdminTimeSlot.objects.create(
                admin=appointment.admin,
                date=appointment.appointment_date,
                start_time=appointment.start_time,
                end_time=appointment.end_time,
                is_booked=True,
                title=appointment.purpose  # You might want to store appointment purpose or other details
            )

            messages.success(request, 'Your appointment has been booked and is waiting for the admin\'s approval.')
            return redirect('appointment_success')
    else:
        form = AppointmentForm()

    return render(request, 'book_appointment.html', {'form': form})


@login_required
def manage_appointments(request):
    pending_appointments = Appointment.objects.filter(admin=request.user, status='P')
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        action = request.POST.get('action')
        appointment = get_object_or_404(Appointment, id=appointment_id)

        if action == 'accept':
            appointment.status = 'A'
            messages.success(request, 'Appointment accepted.')
            # Create a success notification for the user
            Notification.objects.create(
                user=appointment.user,
                message=f"Your appointment with {appointment.admin.username} on {appointment.appointment_date} at {appointment.start_time} has been accepted. Please be present."
            )

        elif action == 'reject':
            appointment.status = 'R'
            messages.success(request, 'Appointment rejected.')
            # Create a rejection notification for the user
            Notification.objects.create(
                user=appointment.user,
                message=f"Your appointment with {appointment.admin.username} on {appointment.appointment_date} at {appointment.start_time} has been rejected."
            )
        appointment.save()
        # Notify the user (similar to the admin notification method)
        return redirect('manage_appointments')

    return render(request, 'manage_appointments.html', {'appointments': pending_appointments})

def appointment_success(request):
    return render(request, 'appointment_success.html')

def calendar(request):
    return render(request, 'calendar.html')
def recurring_event (request):
    return render(request, 'recurring_event.html')

@login_required
def notifications(request):
    user_notifications = Notification.objects.filter(user=request.user)

    # Mark all unread notifications as read
    user_notifications.filter(is_read=False).update(is_read=True)

    return render(request, 'notifications.html', {'notifications': user_notifications})

from datetime import timedelta, datetime

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import Events
from django.shortcuts import render
from django.http import JsonResponse
from .models import Events
from datetime import datetime, timedelta
from .models import Events


# Create your views here.
def index(request):
    all_events = Events.objects.all()
    context = {
        "events": all_events,
    }
    return render(request, 'index.html', context)


from django.http import JsonResponse
from .models import Events


def all_events(request):
    admin = request.user  # Get the currently logged-in user (admin)
    all_events = Events.objects.filter(admin=admin)  # Filter events by admin
    out = []
    for event in all_events:
        out.append({
            'title': event.name,
            'id': event.id,
            'start': event.start.strftime("%m/%d/%Y, %H:%M:%S"),
            'end': event.end.strftime("%m/%d/%Y, %H:%M:%S"),
        })
    return JsonResponse(out, safe=False)



def add_event(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    admin = request.user  # Get the currently logged-in user (admin)
    event = Events(name=str(title), start=start, end=end, admin=admin)
    event.save()
    data = {}
    return JsonResponse(data)



def update(request):
    start = request.GET.get("start", None)
    end = request.GET.get("end", None)
    title = request.GET.get("title", None)
    id = request.GET.get("id", None)
    admin = request.user  # Get the currently logged-in user (admin)

    # Fetch the event only if it belongs to the admin
    event = Events.objects.get(id=id, admin=admin)
    event.start = start
    event.end = end
    event.name = title
    event.save()
    data = {}
    return JsonResponse(data)



def remove(request):
    id = request.GET.get("id", None)
    admin = request.user  # Get the currently logged-in user (admin)

    # Fetch the event only if it belongs to the admin
    event = Events.objects.get(id=id, admin=admin)
    event.delete()
    data = {}
    return JsonResponse(data)


from datetime import timedelta, datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.decorators import login_required

@login_required  # Ensure the user is logged in
@csrf_exempt
def add_recurring_event(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Parse JSON body
            title = data.get('title')
            start_date = data.get('start_date')
            end_date = data.get('end_date')
            start_time = data.get('start_time')
            duration = int(data.get('duration'))  # Convert duration to int
            recurrence = data.get('recurrence')

            # Process the data and add the recurring event logic here
            start_date = datetime.strptime(start_date, "%Y-%m-%d")
            end_date = datetime.strptime(end_date, "%Y-%m-%d")
            start_time = datetime.strptime(start_time, "%H:%M").time()

            # Create the initial event
            initial_event_start = datetime.combine(start_date, start_time)
            initial_event_end = initial_event_start + timedelta(hours=duration)

            # Get the current logged-in user (admin)
            admin_user = request.user

            # Create and save the initial event
            initial_event = Events(
                name=title,
                start=initial_event_start,
                end=initial_event_end,
                is_recurring=True,  # Mark as recurring
                admin=admin_user   # Link event to the logged-in admin
            )
            initial_event.save()

            # Generate subsequent events based on the recurrence type
            current_date = start_date
            while current_date <= end_date:
                if current_date != start_date:  # Skip the first event
                    new_event_start = datetime.combine(current_date, start_time)
                    new_event_end = new_event_start + timedelta(hours=duration)

                    # Create and save the new recurring event
                    new_event = Events(
                        name=title,
                        start=new_event_start,
                        end=new_event_end,
                        is_recurring=True,
                        admin=admin_user  # Link event to the logged-in admin
                    )
                    new_event.save()

                # Increment the date based on recurrence type
                if recurrence == 'daily':
                    current_date += timedelta(days=1)
                elif recurrence == 'weekly':
                    current_date += timedelta(weeks=1)
                elif recurrence == 'monthly':
                    next_month = current_date.month % 12 + 1
                    next_year = current_date.year + (current_date.month // 12)
                    current_date = current_date.replace(year=next_year, month=next_month)

            return JsonResponse({'status': 'Recurring event added successfully'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=400)

    elif request.method == "GET":
        # Render the form for adding recurring events
        return render(request, 'add_recurring_event.html')

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def month (request):
    return render(request, 'month.html')
def week (request):
    return render(request, 'week.html')
def userhome (request):
    return render(request, 'userhome.html')



#fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff


from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Meeting, Invitation,Message
from .forms import MeetingForm

from django.utils import timezone


def create_meeting(request):
    if request.method == 'POST':
        form = MeetingForm(request.POST)
        if form.is_valid():
            meeting = form.save(commit=False)
            meeting.created_by = request.user
            meeting.save()

            invitee_ids = request.POST.getlist('invitees')
            if not invitee_ids:
                messages.error(request, 'Please select at least one invitee.')
                return redirect('create_meeting')

            for invitee_id in invitee_ids:
                try:
                    invitee = User.objects.get(id=invitee_id)
                    Invitation.objects.create(meeting=meeting, invitee=invitee)

                    # Create a message for the invitee
                    message_text = f"You have been invited to a meeting: {meeting.title} on {meeting.date} at {meeting.start_time}."
                    Message.objects.create(user=invitee, message=message_text, meeting=meeting)
                except User.DoesNotExist:
                    print(f"User with ID {invitee_id} does not exist.")

            messages.success(request, 'Invites sent successfully!')
            return redirect('create_meeting')
    else:
        form = MeetingForm()

    users = User.objects.filter(is_staff=False)
    admins = User.objects.filter(is_staff=True)

    return render(request, 'create_meeting.html', {
        'form': form,
        'users': users,
        'admins': admins,
    })


from django.shortcuts import get_object_or_404


from django.shortcuts import get_object_or_404



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Message, Invitation



def view_messages(request):
    messages_list = Message.objects.filter(user=request.user)

    if request.method == 'POST':
        invitation_id = request.POST.get('invitation_id')
        status = request.POST.get('status')
        decline_reason = request.POST.get('decline_reason', '').strip()

        if not status:
            messages.error(request, "Please select either Accept or Decline.")
            return redirect('view_messages')

        invitation = get_object_or_404(Invitation, id=invitation_id, invitee=request.user)

        if status == 'Declined' and not decline_reason:
            messages.error(request, "Please provide a reason for declining the invitation.")
            return redirect('view_messages')

        invitation.status = status
        invitation.decline_reason = decline_reason if status == 'Declined' else ''
        invitation.save()
        messages.success(request, "Your response has been submitted.")

        return redirect('view_messages')

    return render(request, 'view_messages.html', {'messages': messages_list})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Meeting

@login_required
def view_meeting_responses(request):
    # Fetch all meetings created by the logged-in user
    meetings = Meeting.objects.filter(created_by=request.user).prefetch_related('invitations')
    return render(request, 'meeting_status.html', {'meetings': meetings})