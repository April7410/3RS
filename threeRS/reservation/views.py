from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404

from .models import Building, Room, Reservation
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools


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
		send_email(b, r, event_name, date, time_begin, time_end, attendance)
		make_calendar(event_name, date, time_begin, time_end)
		return render(request, 'reserve.html', context)


def send_email(buil, room_, e_name, d, t_begin, t_end, attendees):
	subject = "Reservation Request for " + str(room_)
	message = "The room "+ str(room_) + " has been requested from " + str(t_begin) + " to "+str(t_end)+"\nThere are "+str(attendees)+" people expected to attend. On "+str(d)+" building "+str(buil)+" event name "+e_name
	from_email = settings.EMAIL_HOST_USER
	to_list = [settings.EMAIL_HOST_USER]
	send_mail(subject, message, from_email, to_list, fail_silently=True)


def make_calendar(e_name, d, t_begin, t_end):
	set_time = str(d)+'T'+str(t_begin)+':00-04:00'
	set_end = str(d)+'T'+str(t_end)+':00-04:00'
	SCOPES = 'https://www.googleapis.com/auth/calendar'
	store = file.Storage('C:\\Users\\gateway\\Desktop\\google_cred\\credentials.json')
	creds = store.get()
	print("this is the problem")
	if not creds or creds.invalid:
		flow = client.flow_from_clientsecrets('C:\\Users\\gateway\\Desktop\\google_cred\\this.json', SCOPES)
		creds = tools.run_flow(flow, store)
	service = build('calendar', 'v3', http=creds.authorize(Http()))
	event ={
		'summary': e_name,
		'start': {
			'dateTime': set_time
		},
		'end': {
			'dateTime': set_end
		}
	}
	e = service.events().insert(calendarId='primary', body=event).execute()



