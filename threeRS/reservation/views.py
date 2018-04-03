from django.shortcuts import render, get_object_or_404
from .models import Building, Room, Reservation


def buildings(request):
	buildings = Building.objects.order_by('name')
	context = { 'buildings': buildings }
	return render(request, 'buildings.html', context)

def rooms(request, building_pk):
    b = get_object_or_404(Building, pk=building_pk)
    rooms = Room.objects.filter(building=b).filter(reserved=False).order_by('name')
    context = { 'building': b,
               'rooms': rooms, }
    return render(request, 'rooms.html', context)

def reserve(request, building_pk, room_pk):
	b = get_object_or_404(Building, pk=building_pk)
	queryset = Room.objects.filter(building=b)
	r = get_object_or_404(queryset, pk=room_pk)
	return render(request, 'reserve.html',
				  { 'building': b,
				    'room': r, })
	
def reserve_success(request, building_pk, room_pk):
	b = get_object_or_404(Building, pk=building_pk)
	r = get_object_or_404(Room, building=b, pk=room_pk)
	try:
		event_name = str(request.POST['event_name'])
		date = request.POST['date']
		time_begin = request.POST['time_begin']
		time_end = request.POST['time_end']
		attendance = int(request.POST['attendance'])
	except (KeyError):
		context = { 'building': b,
				   'room': r,
				   'error_message': 'Fill Out Missing Information', }
		return render(request, 'reserve.html', context)
	else:
		r.reserved = True;
		r.save()
		reservation = Reservation(building=b,
								  room=r,
								  event_name=event_name,
								  date=date,
								  time_begin=time_begin,
								  time_end=time_end,
								  attendance=attendance)
		reservation.save()
		context = { 'building': b,
				   'room': r,
				   'success': 'You made a reservation for ' + str(r), }
		return render(request, 'reserve.html', context)