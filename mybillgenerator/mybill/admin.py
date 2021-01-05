from django.contrib import admin
from . models import *

# Register your models here.
admin.site.register(Registration)
admin.site.register(Buildings)
admin.site.register(Readings)
admin.site.register(Calculation)
admin.site.register(Feedback)