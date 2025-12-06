from django.shortcuts import render, redirect
from django.http import HttpResponse
from events.forms import EventModelForm, ParticipantsFormset
from django.contrib import messages
from events.models import Participants, Event, Category
from django.utils import timezone
from datetime import date
from django.db.models import Q

def home(request):
    return render(request, "home.html")

def dashboard(request):
    events = Event.objects.all()
    total_events = events.count()
    upcoming_events = Event.objects.filter(date__gte = date.today()).count()
    past_events = Event.objects.filter(date__lt = date.today()).count()
    todays_events = Event.objects.filter(date = date.today())
    total_participants = Participants.objects.values("email").distinct().count()
    all_participants = None
    type = request.GET.get('type')
    heading = "Today's Events"
    if type == "all_events":
        todays_events = Event.objects.all()
        heading = "All Events"

    elif type == "upcoming_events":
        todays_events = Event.objects.filter(date__gte = date.today())
        heading = "Upcoming Events"

    elif type == "past_events":
        todays_events = Event.objects.filter(date__lt = date.today())
        heading = "Past Events"

    elif type == "all_participants":
        all_participants = Participants.objects.distinct().values("name","email").all()
        heading = "All Participants List"
    context = {
        "total_events" : total_events,
        "all_events" : events,
        "upcoming_events" : upcoming_events,
        "past_events" : past_events,
        "todays_events" : todays_events,
        "heading" : heading,
        "total_participants" : total_participants,
        "all_participants" : all_participants
    }
    return render(request, "dashboard.html", context)

def all_events(request):
    all_event_show = Event.objects.order_by('date')
    return render(request, "all_events.html", {"all_event_show" : all_event_show})

def delete_event(request, id):
    if request.method == "POST":
        event = Event.objects.get(id=id)
        participants = list(event.participants.all())
        participants_to_delete = []

        for p in participants:
            if not p.events.exclude(id=event.id).exists():
                participants_to_delete.append(p)

        for p in participants_to_delete:
            p.delete()

        event.delete()
        return redirect("all-events")

def create_event(request):
    event_form = EventModelForm()
    if request.method == "POST":
        event_form = EventModelForm(request.POST)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Created Successfully!")
            return redirect("form")
    context = {
        "event_form":event_form
    }
    return render(request, "event_form.html", context)

def update_event(request, id):
    event = Event.objects.get(id=id)
    event_form = EventModelForm(instance=event)
    if request.method == "POST":
        event_form = EventModelForm(request.POST, instance=event)
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "Event Updated Successfully!")
            return redirect("event-detail", id=event.id)
    context = {
        "event_form":event_form
    }
    return render(request, "event_form.html", context)

def add_participants(request, id):
    event = Event.objects.get(id=id)
    formset = ParticipantsFormset(queryset=Participants.objects.none())
    if request.method == "POST":
        formset = ParticipantsFormset(request.POST)
        if formset.is_valid():
            participants = formset.save()
            for p in participants:
                event.participants.add(p)
            return redirect("event-detail", id=event.id)
        
    return render(request, "add_participants.html", {"formset": formset})

def detail_event(request, id):
    event = Event.objects.select_related("category").prefetch_related("participants").get(id=id)
    participants = event.participants.all()
    context = {
        "event" : event,
        "participants" : participants 
    }
    return render(request, "event_detail.html", context)

def delete_participants(request, event_id, participant_id):
    if request.method == "POST":
        participant = Participants.objects.get(id=participant_id)
        participant.delete()
        return redirect("event-detail", id=event_id)
    
def home(request):
    query = request.GET.get("value_from_user")
    events = Event.objects.all()
    category_id = request.GET.get("category")
    categories = Category.objects.all()
    if query:
        events = Event.objects.filter(Q(name__icontains=query) | Q(location__icontains=query))
    if category_id:
        events = Event.objects.filter(category__id=category_id)
    context = {
        "query" : query,
        "events" : events,
        "categories" : categories,
        "selected_category" : category_id
    }
    return render(request, "home.html", context)