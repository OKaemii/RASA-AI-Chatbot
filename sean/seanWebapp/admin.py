from django.contrib import admin

from seanWebapp.forms import UserProfile
from seanWebapp.models import Log, Resource

admin.site.register(UserProfile)
admin.site.register(Log)
admin.site.register(Resource)