from __future__ import unicode_literals

from django.db import models
from django.core.validators import *

from django.contrib.auth.models import User, Group

from django.contrib import admin
import base64
class Events(APIView):
	permission_classes = (AllowAny,)
	parser_classes = (parsers.JSONParser,parsers.FormParser)
	renderer_classes = (renderers.JSONRenderer, )

	def get(self, request, format=None):
		events = Event.objects.all()
		json_data = serializers.serialize('json', events)
		content = {'events': json_data}
		return HttpResponse(json_data, content_type='json')

	def post(self, request, *args, **kwargs):
		print 'REQUEST DATA'
		print str(request.data)

		eventtype = request.data.get('eventtype')
		timestamp = int(request.data.get('timestamp'))
		userid = request.data.get('userid')
		requestor = request.META['REMOTE_ADDR']

		newEvent = Event(
			eventtype=eventtype,
			timestamp=datetime.datetime.fromtimestamp(timestamp/1000, pytz.utc),
			userid=userid,
			requestor=requestor
		)

		try:
			newEvent.clean_fields()
		except ValidationError as e:
			print e
			return Response({'success':False, 'error':e}, status=status.HTTP_400_BAD_REQUEST)

		newEvent.save()
		print 'New Event Logged from: ' + requestor
		return Response({'success': True}, status=status.HTTP_200_OK)

class Event(models.Model):
	eventtype = models.CharField(max_length=1000, blank=False)
	timestamp = models.DateTimeField()
	userid = models.CharField(max_length=1000, blank=True)
	requestor = models.GenericIPAddressField(blank=False)

	def __str__(self):
		return str(self.eventtype)

class EventAdmin(admin.ModelAdmin):
	list_display = ('eventtype', 'timestamp')


class ApiKey(models.Model):
	owner = models.CharField(max_length=1000, blank=False)
	key = models.CharField(max_length=5000, blank=False)

	def __str__(self):
		return str(self.owner) + str(self.key)

class ApiKeyAdmin(admin.ModelAdmin):
	list_display = ('owner','key')
