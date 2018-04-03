from django.db import models
from django.urls import reverse
from django.utils.encoding import smart_text

class Building(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Room(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    reserved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.building) + ": " + self.name

    def is_reserved(self):
        return self.reserved

class Reservation(models.Model):
	#account = models.ForeignKey('signup.SignUp', on_delete=models.CASCADE)
	building = models.ForeignKey(Building, on_delete=models.CASCADE)
	room = models.ForeignKey(Room, on_delete=models.CASCADE)
	event_name = models.CharField("Event Name", max_length=30)
	date = models.DateField("Date")
	time_begin = models.TimeField("Time Begin")
	time_end = models.TimeField("Time End")
	attendance = models.PositiveSmallIntegerField("Attendance", default=0)
	timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    
	def get_absolute_url(self):
		return reverse('reservation:detail', kwargs={'reservation_pk' : self.pk})
    
	def __str__(self):
		return smart_text(self.event_name + " @ " + str(self.room) +
						  " (" + str(self.time_begin) + " - " +
						  str(self.time_end) + ")")