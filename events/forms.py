from django import forms
from events.models import Event, Participants
from django.forms import modelformset_factory

class EventModelForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ["category", "name", "description", "date", "time", "location"]
        widgets = {
            "category": forms.Select(attrs={
                "class": "w-full px-4 py-2 rounded-lg border border-gray-300"
            }),
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 rounded-lg border border-gray-300"
            }),
            "description": forms.Textarea(attrs={
                "rows": 4,
                "class": "w-full px-4 py-2 rounded-lg border border-gray-300"
            }),
            "date": forms.DateInput(attrs={
                "type": "date",
                "class": "w-full px-4 py-2 rounded-lg border border-gray-300"
            }),
            "time": forms.TimeInput(attrs={
                "type": "time",
                "class": "w-full px-4 py-2 rounded-lg border border-gray-300"
            }),
            "location": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 rounded-lg border border-gray-300"
            }),
        }

class ParticipantsForm(forms.ModelForm):
    class Meta:
        model = Participants
        fields = ["name", "email"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-2 rounded-lg border border-gray-300"
            }),
            "email": forms.EmailInput(attrs={"class": "w-full px-4 py-2 rounded-lg border border-gray-300"})
        }
        
ParticipantsFormset = modelformset_factory(Participants, form=ParticipantsForm, extra=3, fields=["name", "email"])