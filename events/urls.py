from django.contrib import admin
from django.urls import path
from events.views import home, dashboard, create_event, all_events, delete_event, detail_event, update_event, add_participants, delete_participants

urlpatterns = [
    path('', home, name="home"),
    path("dashboard", dashboard, name="dashboard"),
    path("addevent", create_event, name="form"),
    path("all_events", all_events, name="all-events"),
    path('delete-event/<int:id>/', delete_event, name='delete-event'),
    path('event_detail/<int:id>/', detail_event, name="event-detail"),
    path('update_event/<int:id>/', update_event, name="update-event"),
    path('add_participants/<int:id>/', add_participants, name="add-participants"),
    path('delete-participant/<int:event_id>/<int:participant_id>/', delete_participants, name='delete-participant')
]
