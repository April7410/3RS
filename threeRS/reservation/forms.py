from .models import Reservation
from django.forms import ModelForm

class ReserveForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('event_name', 'date', 'time_begin', 'time_end', 'attendance')