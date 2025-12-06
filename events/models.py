from django.db import models

class Category(models.Model):
    CATEGORY_CHOICES = (
        ("MUSIC", "Music"),
        ("TECHNOLOGY", "Technology"),
        ("ART", "Art"),
        ("SPORTS", "Sports"),
        ("EDUCATION", "Education"),
        ("OTHERS", "Others")
    )
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.get_category_display()

class Participants(models.Model):
    name = models.CharField(max_length=250)
    email = models.EmailField()

class Event(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=6)
    name = models.CharField(max_length=250)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField(help_text="HH:MM:SS")
    location = models.CharField(max_length=250)
    participants = models.ManyToManyField(Participants, related_name="events")